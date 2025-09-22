# AlBeSa – Art Guide Project

## Overview
This project explores how artificial intelligence can support museum and gallery visitors by providing accessible, immediate, and personalized information about artworks. Our solution is a mobile application that allows users to take a photo of an artwork and receive a spoken and written explanation, enriched with historical and contextual details.  

The project follows a structured process: problem definition, data collection and processing, model design and training, and software/tool integration.  

---

## Problem Definition
Visitors often struggle with limited or inaccessible information in museums and cultural spaces. Labels are short, guided tours are not always available, and accessibility for international visitors or visually impaired people is limited.  
We aim to solve this by combining artwork recognition with contextual explanations, presented in both audio and text formats.

---

## Data
We focus on creating curated datasets for specific expositions in collaboration with stakeholders (e.g., curators). Each dataset contains:
- **Inputs**: images of artworks, artist names, periods/styles.  
- **Outputs (labels)**: metadata (artist, period, context).  

**Exploration (Big Data 4Vs):**
- **Volume**: manageable size (hundreds of artworks per exposition).  
- **Velocity**: static dataset with occasional updates (per new exhibition).  
- **Variety**: images (JPEG/PNG) + structured metadata (CSV/Excel).  
- **Veracity**: sources from museum catalogues, Wikipedia, and curators ensure reliability.  

Data preprocessing includes cleaning inconsistent metadata, aligning input–output pairs, resizing images, and splitting into **train/dev/test** sets.

---

## Model
Our system combines:  
1. **Image embeddings** for artwork recognition.  
2. **LLM layer** to generate user-friendly contextual descriptions.  

**Steps:**  
- Train embedding-based classifier for artist recognition.  
- Use an LLM (via API) with system prompts to transform raw metadata into accessible descriptions.  
- Evaluate on metrics such as recognition accuracy (>85%) and response time (<10s).  

**Statistics (expected):**  
- Training time: several hours depending on dataset size.  
- Epochs: ~20–30 for convergence.  
- Evaluation metrics: recognition accuracy, inference latency, user satisfaction (pilot tests).  

---

## Software Used
- **Data processing**: `pandas`, `numpy`.  
- **Model training & embeddings**: Hugging Face Transformers, PyTorch.  
- **Text generation & contextualization**: LangChain, Gemini API.  
- **Interface & prototyping**: Google Colab, Streamlit (for demos).  
- **Version control**: Git/GitHub.  

---

## References
- Wikipedia/Wikidata API for metadata.  
- OpenArt, WikiArt, and museum open collections for images.  
- Hulten, G. (2018). *Building Intelligent Systems: A Guide to Machine Learning Engineering*.  
- Chacon, S., Straub, B. (2020). *Pro Git*.  
