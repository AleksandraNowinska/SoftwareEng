"""
Art Guide - AI-Powered Artwork Recognition System
Main application file for standalone/monolithic deployment.

This application uses CLIP embeddings and FAISS vector search to identify
artworks from user-uploaded photos, then generates descriptive explanations.

For distributed deployment, see the distributed/ directory.

Authors: AlBeSa Team (Beloslava Malakova, Alicja Gwiazda, 
         Stanimir Dimitrov, Aleksandra Nowińska)
Version: 1.0
"""

import os
import time
import csv
import gradio as gr
import faiss
import numpy as np
import pandas as pd
from PIL import Image

# Pre-load torch to avoid slow dynamic compilation during transformers import
import torch
torch.set_num_threads(1)  # Reduce overhead

# Now import transformers (which triggers torchvision)
from transformers import CLIPProcessor, CLIPModel

# LLM Integration (Gemini API)
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("Warning: langchain-google-genai not installed. Using placeholder descriptions.")

# ============================================================================
# Configuration
# ============================================================================

# Load CLIP model for embeddings
device = "cuda" if torch.cuda.is_available() else "cpu"
clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# ============================================================================
# Data Loading
# ============================================================================

# Paths (adjust as needed)
INDEX_PATH = "models/faiss.index"
META_PATH = "models/metadata.parquet"
LOG_PATH = "app/logs/telemetry.csv"
SAMPLE_IMAGES_DIR = "data/sample_images/"

# Load FAISS index + metadata
if os.path.exists(INDEX_PATH) and os.path.exists(META_PATH):
    index = faiss.read_index(INDEX_PATH)
    metadata = pd.read_parquet(META_PATH)
else:
    index = None
    metadata = pd.DataFrame(columns=["artist", "title", "period", "image_path"])

# Ensure log directory
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
if not os.path.exists(LOG_PATH):
    with open(LOG_PATH, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "artist", "confidence", "response_time"])

# Initialize Gemini LLM (if API key available)
gemini_llm = None
if GEMINI_AVAILABLE:
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if api_key:
        try:
            gemini_llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",  # Using Flash for faster responses
                google_api_key=api_key,
                temperature=0.7
            )
            print("✓ Gemini LLM initialized successfully")
        except Exception as e:
            print(f"Warning: Failed to initialize Gemini LLM: {e}")
            gemini_llm = None
    else:
        print("Info: GOOGLE_API_KEY not set. Using placeholder descriptions.")


# ============================================================================
# Core AI Functions
# ============================================================================

def embed_image(img: Image.Image) -> np.ndarray:
    """
    Generate CLIP embedding for an input image.
    
    This function processes an image using the CLIP model to generate a 512-dimensional
    embedding vector that captures semantic visual features. The embedding is L2-normalized
    to enable cosine similarity comparisons in the vector database.
    
    Args:
        img (PIL.Image.Image): Input image in PIL format. Should be RGB mode.
        
    Returns:
        np.ndarray: L2-normalized embedding vector of shape (1, 512) with dtype float32.
                   The normalization ensures ||embedding|| = 1.0 for cosine similarity.
    
    Example:
        >>> from PIL import Image
        >>> img = Image.open("artwork.jpg")
        >>> embedding = embed_image(img)
        >>> embedding.shape
        (1, 512)
        >>> np.linalg.norm(embedding)  # Should be ~1.0
        1.0
    
    Notes:
        - Uses GPU if available (cuda) for faster inference
        - Preprocessing (resizing, normalization) is handled by CLIPProcessor
        - No gradients are computed (inference only)
    """
    inputs = clip_processor(images=img, return_tensors="pt").to(device)
    with torch.no_grad():
        emb = clip_model.get_image_features(**inputs)
    emb = emb.cpu().numpy().astype("float32")
    emb /= np.linalg.norm(emb)  # L2 normalization for cosine similarity
    return emb


def search_index(img: Image.Image, k: int = 5):
    """
    Search the FAISS vector database for similar artworks.
    
    Generates an embedding for the input image and queries the FAISS index
    to find the k most similar artworks based on L2 distance in embedding space.
    
    Args:
        img (PIL.Image.Image): Query image to search for
        k (int): Number of top results to return (default: 5)
        
    Returns:
        tuple: (results_df, embedding) where:
            - results_df (pd.DataFrame): Top-k results with columns [artist, title, period, 
                                        image_path, distance]. Sorted by distance (ascending).
            - embedding (np.ndarray): The query image embedding (1, 512)
            
            Returns (None, None) if index is not loaded or empty.
    
    Example:
        >>> img = Image.open("photo.jpg")
        >>> results, emb = search_index(img, k=3)
        >>> results[['artist', 'distance']]
                   artist  distance
        0       Van Gogh      0.15
        1          Monet      0.23
        2        Picasso      0.31
    
    Notes:
        - Lower distance = higher similarity
        - FAISS uses L2 distance, not cosine (but embeddings are normalized)
        - Returns None if no index is loaded (graceful degradation)
    """
    if index is None or len(metadata) == 0:
        return None, None

    emb = embed_image(img)
    D, I = index.search(emb, k)
    results = metadata.iloc[I[0]].copy()
    results["distance"] = D[0]
    return results, emb


def generate_description(artist: str, title: str, period: str) -> str:
    """
    Generate a descriptive explanation of an artwork using Gemini LLM.
    
    Provides contextual, tour-guide style descriptions of artworks. Falls back
    to template-based descriptions if Gemini API is not available.
    
    Args:
        artist (str): Name of the artist
        title (str): Title of the artwork
        period (str): Historical period or artistic movement
        
    Returns:
        str: Human-readable description including artist background,
             period context, and artistic significance (2-3 paragraphs).
    
    Example:
        >>> desc = generate_description("Vincent van Gogh", "Starry Night", "Post-Impressionism")
        >>> print(desc[:100])
        "The Starry Night" by Vincent van Gogh is one of the most iconic paintings...
    
    Notes:
        - Uses Gemini 1.5 Flash if GOOGLE_API_KEY environment variable is set
        - Falls back to placeholder template if API unavailable
        - Response typically 150-300 words in tour-guide conversational style
    """
    if gemini_llm is not None:
        try:
            system_prompt = """You are a knowledgeable and engaging museum tour guide. 
Your role is to provide accessible, conversational explanations of artworks to visitors 
with varying levels of art knowledge. Keep descriptions between 150-250 words.

Include:
1. Brief artist background and their significance
2. Historical/cultural context of the period
3. Notable features or techniques in this specific work
4. Why this artwork matters in art history

Use a warm, enthusiastic tone that makes art accessible to everyone."""

            user_query = f"Tell me about '{title}' by {artist} from the {period} period."
            
            response = gemini_llm.invoke([
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ])
            
            return response.content
        except Exception as e:
            print(f"Warning: Gemini API call failed: {e}. Using placeholder.")
            # Fall through to placeholder
    
    # Placeholder fallback (when Gemini unavailable)
    return f"""This is '{title}' by {artist}, created during the {period} period.

{artist} was a renowned artist whose work exemplified the {period} movement. 
This particular piece showcases the characteristic techniques and themes of that era, 
including innovative use of color, composition, and subject matter.

The artwork holds significant cultural and historical importance, representing 
a key moment in the evolution of art. For more detailed information about this 
specific work, please consult museum resources or art historical databases.

Note: Full AI-generated descriptions require Gemini API configuration."""


# ============================================================================
# Main Recognition Pipeline
# ============================================================================

def recognize(img, show_context):
    """
    Main recognition pipeline: image → embedding → search → description.
    
    Orchestrates the complete workflow from user image to final description,
    including telemetry logging for monitoring and analytics.
    
    Args:
        img (PIL.Image.Image): User-uploaded artwork image
        show_context (bool): If True, include similar artworks in description
        
    Returns:
        tuple: (label, preview_image, description) where:
            - label (str): Recognition result with artist and confidence
            - preview_image (PIL.Image.Image): The input image for display
            - description (str): Generated description (+ context if requested)
    
    Example:
        >>> img = Image.open("photo.jpg")
        >>> label, img_preview, desc = recognize(img, show_context=True)
        >>> print(label)
        Recognized: Van Gogh (confidence 0.9234)
        >>> print(desc[:50])
        This is 'Starry Night' by Van Gogh, created in...
    
    Side Effects:
        - Logs request to telemetry CSV (timestamp, artist, confidence, response_time)
        - Prints are for debugging (remove in production)
    
    Error Handling:
        - Returns error message if no index loaded
        - Gracefully handles search failures
    """
    start_time = time.time()
    results, emb = search_index(img, k=5)

    if results is None:
        return "No index loaded.", None, "N/A"

    # Top-1 recognition
    top1 = results.iloc[0]
    artist, title, period, conf = (
        top1["artist"],
        top1.get("title", "Unknown"),
        top1.get("period", "Unknown"),
        float(top1["distance"]),
    )

    description = generate_description(artist, title, period)
    response_time = round(time.time() - start_time, 2)

    # Log telemetry
    with open(LOG_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), artist, conf, response_time])

    if show_context:
        neighbors = results[["artist", "title", "period", "distance"]].to_dict(orient="records")
        return f"Recognized: {artist} (confidence {conf:.4f})", img, description + "\nContext: " + str(neighbors)
    else:
        return f"Recognized: {artist} (confidence {conf:.4f})", img, description


# ============================================================================
# User Interface (Gradio)
# ============================================================================

# Collect sample images for quick demo
sample_images = []
if os.path.exists(SAMPLE_IMAGES_DIR):
    for file in os.listdir(SAMPLE_IMAGES_DIR):
        if file.lower().endswith((".jpg", ".jpeg", ".png")):
            sample_images.append(os.path.join(SAMPLE_IMAGES_DIR, file))

# ============================================================================
# Gradio Interface Definition
# ============================================================================

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("# 🖼️ Art Guide – Demo App")
    gr.Markdown("Upload an artwork photo to receive AI-powered recognition and description.")
    
    with gr.Row():
        with gr.Column():
            img_input = gr.Image(type="pil", label="Upload artwork photo")
            sample = gr.Dropdown(sample_images, label="Or choose a sample image", type="value")
            show_context = gr.Checkbox(label="Show retrieved context", value=False)
            run_btn = gr.Button("Recognize Artwork")
        with gr.Column():
            label_output = gr.Textbox(label="Recognition Result")
            img_output = gr.Image(label="Preview")
            desc_output = gr.Textbox(label="Description")

    def run_pipeline(uploaded, sample_path, show_context):
        if uploaded is None and sample_path:
            uploaded = Image.open(sample_path)
        if uploaded is None:
            return "No image provided", None, "Please upload or select a sample."
        return recognize(uploaded, show_context)

    run_btn.click(run_pipeline, inputs=[img_input, sample, show_context], outputs=[label_output, img_output, desc_output])


# ============================================================================
# Application Entry Point
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("🎨 Art Guide - AI-Powered Artwork Recognition")
    print("=" * 60)
    print(f"Device: {device.upper()}")
    print(f"Model: CLIP ViT-B/32")
    print(f"Index: {INDEX_PATH}")
    print(f"Artworks loaded: {len(metadata)}")
    print("=" * 60)
    print("Starting Gradio interface at http://localhost:7860")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    demo.launch(server_name="0.0.0.0", server_port=7860)
