# AlBeSa – Art Guide Project

## Overview
This project explores how artificial intelligence can support museum and gallery visitors by providing accessible, immediate, and personalized information about artworks. Our solution is a mobile/web application that allows users to take a photo of an artwork and receive a spoken and written explanation, enriched with historical and contextual details.

**Team:** AlBeSa  
**Authors:** Beloslava Malakova, Alicja Gwiazda, Stanimir Dimitrov, Aleksandra Nowińska  
**Institution:** TU/e  
**Course:** Software Engineering for AI Systems  
**Date:** November 2025

---

## 🎯 Problem Definition
Visitors often struggle with limited or inaccessible information in museums and cultural spaces. Labels are short, guided tours are not always available, and accessibility for international visitors or visually impaired people is limited.

We aim to solve this by combining artwork recognition with contextual explanations, presented in both audio and text formats.

---

## 🏗️ Architecture

The system is available in two deployment modes:

### 1. Monolithic Deployment (`app.py`)
Single-server deployment for development and small-scale use.
- Gradio web interface
- CLIP embeddings + FAISS vector search
- Placeholder LLM integration
- **Access:** `http://localhost:7860`

### 2. Distributed Architecture (`distributed/`)
Production-ready three-tier architecture:
- **Interface Server** (Flask, port 5000): User-facing UI
- **Orchestrator** (Redis): Message queue for async communication
- **AI Server** (Background): CLIP + FAISS + LLM inference

**Advantages:** Scalable, fault-tolerant, supports multiple concurrent AI servers

---

## 📊 Data

We focus on creating curated datasets for specific expositions in collaboration with stakeholders (e.g., curators). Each dataset contains:
- **Inputs:** Images of artworks, artist names, periods/styles
- **Outputs (labels):** Metadata (artist, period, context)

**Exploration (Big Data 4Vs):**
- **Volume:** Manageable size (hundreds of artworks per exposition)
- **Velocity:** Static dataset with occasional updates (per new exhibition)
- **Variety:** Images (JPEG/PNG) + structured metadata (CSV/Excel)
- **Veracity:** Sources from museum catalogs, Wikipedia, and curators ensure reliability

Data preprocessing includes cleaning inconsistent metadata, aligning input–output pairs, resizing images, and splitting into **train/dev/test** sets.

---

## 🤖 Model

Our system combines:
1. **Image embeddings** for artwork recognition (CLIP ViT-B/32)
2. **Vector similarity search** (FAISS)
3. **LLM layer** to generate user-friendly contextual descriptions (Gemini API)

**Pipeline:**
```
User Image → CLIP Embedding (512-dim) → FAISS Search → Top-5 Results → LLM Description → User
```

**Statistics:**
- **Recognition Accuracy:** 87% top-1, 96% top-5
- **Response Time:** <10 seconds end-to-end
- **Inference Time:** ~1-2 seconds (CPU), <0.5s (GPU)
- **Training:** None (uses pre-trained CLIP)

---

## 🛠️ Software Stack

- **Language:** Python 3.9+
- **Data Processing:** `pandas`, `numpy`
- **ML/Deep Learning:** `torch`, `transformers` (CLIP)
- **Vector Search:** `faiss-cpu`
- **LLM Integration:** `langchain`, `langchain-google-genai`
- **UI:** `gradio`, `streamlit`
- **Web Framework:** `flask` (distributed mode)
- **Message Queue:** `redis`
- **Testing:** `pytest`, `pytest-cov`
- **Version Control:** Git/GitHub

---

## 🚀 How to Run

### Prerequisites

```bash
# Clone repository
git clone https://github.com/AleksandraNowinska/SoftwareEng.git
cd SoftwareEng

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate   # macOS/Linux
# venv\Scripts\activate    # Windows

# Install dependencies
pip install -r requirements.txt
```

### Option 1: Monolithic Deployment (Quick Start)

```bash
python app.py
```

Access at: **http://localhost:7860**

### Option 2: Distributed Deployment (Production)

**Step 1: Start Redis**
```bash
# macOS
brew install redis
brew services start redis

# Linux
sudo apt-get install redis-server
sudo systemctl start redis

# Docker
docker run -d -p 6379:6379 redis:alpine
```

**Step 2: Run Distributed System**
```bash
chmod +x distributed/start_system.sh
./distributed/start_system.sh
```

**Or manually:**
```bash
# Terminal 1: Setup orchestrator
python distributed/orchestrator.py

# Terminal 2: Start AI server
python distributed/ai_server.py

# Terminal 3: Start interface server
python distributed/interface_server.py
```

Access at: **http://localhost:5000**

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=app --cov-report=html

# Run specific test file
pytest tests/test_unit.py -v
pytest tests/test_integration.py -v
```

**Test Coverage:**
- 29 automated tests (18 unit, 11 integration)
- 85%+ code coverage
- Tests: embedding generation, image processing, vector search, metadata retrieval, LLM prompts, end-to-end pipeline

---

## 📁 Project Structure

```
SoftwareEng/
├── app.py                          # Monolithic application
├── requirements.txt                # Python dependencies
├── settings.yaml                   # Configuration
├── README.md                       # This file
├── FINAL_REPORT.md                 # Comprehensive project report
│
├── distributed/                    # Distributed architecture
│   ├── interface_server.py         # User-facing server (port 5000)
│   ├── ai_server.py                # AI inference server
│   ├── orchestrator.py             # Redis message queue setup
│   ├── start_system.sh             # Startup script
│   └── README.md                   # Distributed architecture docs
│
├── tests/                          # Automated tests
│   ├── test_unit.py                # Unit tests (18 tests)
│   ├── test_integration.py         # Integration tests (11 tests)
│   └── __init__.py
│
├── our_tasks_and_solutions/        # Course task submissions
│   ├── task 1                      # Problem definition
│   ├── task 2                      # Data & AI model
│   ├── Task_3_SRS_Document.md      # Software requirements
│   ├── task 4 and 3                # Agile/Git setup
│   ├── task 5                      # Testing implementation
│   ├── task 6                      # Distributed architecture
│   ├── task 7 addendum             # VSD & environmental impact
│   └── tasks 1-7 description       # Assignment descriptions
│
├── app/logs/                       # Telemetry logs
│   └── telemetry.csv
│
├── data/                           # Datasets
│   ├── sample_images/              # Demo images
│   └── sample_dataset.csv
│
├── models/                         # (Not in repo - generated locally)
│   ├── faiss.index                 # Vector database
│   └── metadata.parquet            # Artwork metadata
│
└── prompts/                        # System prompts for LLM
    └── system.md
```

---

## 📝 Documentation

- **[FINAL_REPORT.md](FINAL_REPORT.md)** - Complete project report (all tasks 1-7)
- **[Task_3_SRS_Document.md](our_tasks_and_solutions/Task_3_SRS_Document.md)** - Software Requirements Specification
- **[distributed/README.md](distributed/README.md)** - Distributed architecture guide
- **Inline code documentation** - Comprehensive docstrings in all modules

---

## 🎯 Key Features

✅ **AI-Powered Recognition:** CLIP-based artwork identification (87% accuracy)  
✅ **Fast Response:** <10 seconds end-to-end processing  
✅ **Accessibility:** Text and audio descriptions  
✅ **Scalable Architecture:** Distributed design supports 50+ concurrent users  
✅ **Curator-Friendly:** Upload custom datasets for exhibitions  
✅ **Privacy-First:** No permanent storage of user images  
✅ **Production-Ready:** Comprehensive tests, monitoring, documentation  

---

## 📈 Performance Metrics

| Metric | Target | Achieved |
|--------|--------|----------|
| Recognition Accuracy (top-1) | ≥85% | 87% |
| Recognition Accuracy (top-5) | ≥95% | 96% |
| Response Time | <10s | 8-10s |
| Concurrent Users | 50+ | Tested with 50 |
| Test Coverage | ≥80% | 85% |

---

## 🌍 Environmental Impact

**Carbon Footprint:** ~150 kg CO2/year (moderate usage, 1000 requests/day)
- Uses pre-trained CLIP (avoids training emissions: ~100+ tons CO2)
- Inference: ~0.001 kWh per request
- Future optimizations: Model quantization, edge deployment, carbon-aware scheduling

See [FINAL_REPORT.md](FINAL_REPORT.md) for detailed environmental analysis.

---

## 🤝 Team & Contributions

| Name | Role | Contributions |
|------|------|---------------|
| Aleksandra Nowińska | Scrum Master (Sprint 1) | Data preprocessing, evaluation pipeline, test dataset |
| Stanimir Dimitrov | Scrum Master (Sprint 2) | Vector DB research, embedding generation, retrieval |
| Alicja Gwiazda | Developer | LLM integration, prompt engineering, UI development |
| Beloslava Malakova | Scrum Master (Sprint 3) | Documentation, distributed architecture, testing |

---

## 📚 References

**Datasets:**
- [Best Artworks of All Time (Kaggle)](https://www.kaggle.com/datasets/ikarus777/best-artworks-of-all-time/data)
- [WikiArt Dataset](https://www.kaggle.com/datasets/steubk/wikiart)

**Models:**
- [OpenAI CLIP](https://github.com/openai/CLIP)
- [FAISS Vector Search](https://github.com/facebookresearch/faiss)
- [Gemini API](https://ai.google.dev/)

**Literature:**
- Hulten, G. (2018). *Building Intelligent Systems: A Guide to Machine Learning Engineering*
- Chacon, S., Straub, B. (2020). *Pro Git*

---

## 📄 License

This project is developed as part of academic coursework at TU/e. All rights reserved by the authors.

---

## 🔗 Links

- **GitHub (Main):** https://github.com/AleksandraNowinska/SoftwareEng
- **GitHub (Team):** https://github.com/alicegwiazda/822196_SE
- **Trello Board:** [Project Management](https://trello.com) (Private)

---

## 📞 Contact

For questions or collaboration opportunities, please contact the team through GitHub or university email.

**Last Updated:** November 20, 2025
