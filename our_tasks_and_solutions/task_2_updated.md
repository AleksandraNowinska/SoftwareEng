Task 2 - From Data to AI (Updated)
AlBeSa

Authors: Beloslava Malakova (TU/e: 1923404), Alicja Gwiazda(TU/e:2017830),  
Stanimir Dimitrov(TU/e: 1932217), Aleksandra Nowińska (TU/e: 2008580)

---

## Data

For our project, we work with artwork images sourced from Kaggle's art datasets (Best Artworks of All Time and WikiArt), focusing on data relevant to our stakeholder's needs - a museum curator. The dataset has been curated to include 5 renowned artists (Leonardo da Vinci, Claude Monet, Pablo Picasso, Rembrandt van Rijn, and Vincent van Gogh), with 10 high-quality images per artist, totaling 50 artworks in our vector database.

- **Volume:** 50 curated artwork images (expandable to thousands from full Kaggle datasets)  
- **Variety:** Multiple modalities - visual data (JPEG/PNG images) and metadata (artist names, periods, titles)  
- **Velocity:** Static dataset suitable for offline processing and one-time vector embedding generation  
- **Veracity:** High quality - all images manually verified, no missing data or corrupted files

The data is organized in `data/artworks/<artist_name>/` directories and processed using our custom dataset preparation script (`scripts/prepare_dataset.py`) which generates:
1. FAISS vector index (`models/faiss.index`) - 50 embeddings of 512 dimensions each
2. Metadata file (`models/metadata.parquet`) - Parquet format for efficient querying

This curated subset represents one exhibition scenario, enabling fast similarity search while maintaining high recognition accuracy.

## Model (Pipeline)

Our system uses a Retrieval-Augmented Generation (RAG) pipeline leveraging pre-trained foundation models. The process workflow is:

1. **Embedding Generation:** User uploads artwork image → CLIP ViT-B/32 model generates 512-dimensional embedding (L2-normalized for cosine similarity)
2. **Vector Search:** FAISS searches the vector database for top-5 most similar artworks using L2 distance
3. **Retrieval:** System retrieves metadata (artist, title, period) for matched artworks
4. **Description:** LLM generates tour-guide style description (currently template-based, Gemini API integration planned via LangChain)

### Model Statistics

- **CLIP Model:** Pre-trained ViT-B/32 (no fine-tuning required - transfer learning)
- **Inference Time:** ~0.1-0.3 seconds per image embedding on CPU
- **Search Time:** <10ms for top-5 retrieval from 50-artwork index
- **End-to-End Latency:** <0.5 seconds average
- **Accuracy:** ~85% top-1 accuracy on manual evaluation
- **Vector Dimension:** 512 (CLIP standard)
- **Index Build Time:** ~30 seconds for 50 images
- **Training Epochs:** N/A (using pre-trained model, no custom training)

### Data Processing Pipeline

1. Collect images from Kaggle datasets
2. Organize into artist-specific directories
3. Run `scripts/prepare_dataset.py` to:
   - Load CLIP model
   - Generate embeddings for each image
   - L2-normalize embeddings
   - Build FAISS index
   - Create metadata parquet file
4. Deploy index to production (monolithic or distributed)

## Software Used for Development

**Primary Language:** Python 3.9+

**Data Processing:**
- Kaggle - Dataset source (Best Artworks of All Time, WikiArt)
- Pandas - Metadata management and parquet file handling
- Pillow (PIL) - Image preprocessing and validation

**AI/ML Stack:**
- CLIP (openai/clip-vit-base-patch32) - Image embedding model
- PyTorch - Deep learning framework (CLIP backend)
- Transformers (Hugging Face) - Model loading and inference
- FAISS - Vector similarity search engine
- LangChain - RAG pipeline orchestration (planned for full LLM integration)
- Gemini API - LLM for tour-guide descriptions (architecture ready, not yet fully integrated)

**Application Framework:**
- Gradio - UI for monolithic deployment (`app.py`)
- Flask - Interface Server for distributed deployment
- Redis - Message queue orchestrator for distributed system

**Testing & Quality:**
- pytest - Unit and integration testing (29 tests)
- pytest-cov - Code coverage measurement

**DevOps & Version Control:**
- VS Code - Development environment
- GitHub - Version control and collaboration
- Git - Feature branching and commit management

**Distributed System:**
- Redis - Message broker for inter-service communication
- Docker (optional) - Containerization for deployment

## References

a. https://www.kaggle.com/datasets/ikarus777/best-artworks-of-all-time/data  
b. https://www.kaggle.com/datasets/steubk/wikiart  
c. https://github.com/openai/CLIP  
d. https://github.com/facebookresearch/faiss
