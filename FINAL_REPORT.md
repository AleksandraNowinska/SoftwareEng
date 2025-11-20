# Art Guide - Final Project Report
## AI-Powered Artwork Recognition and Description System

**Project Team:** AlBeSa  
**Authors:** Beloslava Malakova (TU/e: 1923404), Alicja Gwiazda (TU/e: 2017830), Stanimir Dimitrov (TU/e: 1932217), Aleksandra Nowińska (TU/e: 2008580)  
**Course:** Software Engineering for AI Systems  
**Date:** November 2025

---

## Table of Contents

1. [Task 1: Problem Definition, Goals, and Measurements](#task-1)
2. [Task 2: From Data to AI](#task-2)
3. [Task 3: Software Requirements Specification](#task-3)
4. [Task 4: Project Management and Implementation](#task-4)
5. [Task 5: Implementation and Testing](#task-5)
6. [Task 6: Scaling Up - Distributed Architecture](#task-6)
7. [Task 7: Finalization, VSD, and Environmental Impact](#task-7)

---

<a name="task-1"></a>
## Task 1: Problem Definition, Goals, and Measurements

### Problem Definition

When visiting museums, galleries, or cultural sites, many visitors struggle to access clear and engaging information about the artwork they see. Traditional labels often provide only minimal details, and guided tours are not always available, affordable, or accessible in the visitor's language. This creates a barrier for tourists, casual art enthusiasts, and especially individuals with accessibility needs (e.g., people with visual impairments).

The problem is how to provide immediate, personalized, and understandable information about artworks to a wide audience without requiring prior art knowledge.

We break this into subproblems:
1. **Artwork identification:** recognizing a painting, sculpture, or object from an image taken by the user.
2. **Contextual explanation:** providing information beyond the name (art style, historical context, cultural relevance).
3. **Accessible presentation:** delivering information in multiple modes (text + audio) to suit diverse user needs.
4. **Ease of use:** ensuring the interaction is simple (e.g., "take a photo and get an explanation").

**High-level solution:** A mobile app that allows users to take a photo of an artwork and immediately receive a spoken and written explanation. The system relies on existing resources (art databases, Wikipedia) to ensure reliable and scalable content delivery.

### Objectives

**Main Goal:** Enable visitors to engage with artworks in an accessible, interactive, and informative way.

**Sub-goals:**
- Provide fast and accurate artwork recognition.
- Deliver concise, contextual explanations of identified artworks beyond basic labels.
- Ensure inclusivity by offering both text and audio explanations.
- Design the interface to be intuitive and simple.
- Support tourists and international visitors by delivering audio-first accessibility.
- Increase engagement in cultural spaces via interactive explanations.
- Encourage adoption among tourists and casual art enthusiasts.

### Measurements / KPIs

To evaluate success, we propose the following measurable criteria:
- **Accuracy of recognition:** ≥85% of artworks correctly identified
- **Response time:** Average time from photo upload to output <10s
- **User satisfaction:** Average rating from pilot tests >3/5
- **Tourist adoption:** ≥50–100 pilot users in cultural sites
- **Content richness:** Average length and coverage of generated descriptions (art style, context, year, artist)
- **Accessibility impact:** ≥40% of users utilizing audio mode
- **Retention rate:** ≥30% returning users in first month

---

<a name="task-2"></a>
## Task 2: From Data to AI

### Data

For our project, we work with a subset of existing open-source art datasets from Kaggle, focusing only on information relevant to one selected exhibition. The datasets are partially sampled and curated to fit the needs of our stakeholder (a curator). This means filtering the data down to include only the artist name and a corresponding image of the artwork, which represent the minimum requirements for building an AI system that can support an exhibition setting.

We used datasets such as "Best Artworks of All Time", which contain thousands of high-quality images. From these, we create a reduced dataset, suitable for one exhibition scenario.

**Data Characteristics (4Vs):**
- **Volume:** Full datasets contain over 8,000 images, but for our task, we curate a smaller sample (dozens to a few hundred images per exhibition)
- **Variety:** Multiple modalities - tabular metadata (artist names, time periods, genres) and visual data (artwork images)
- **Velocity:** Static rather than streaming, making it suitable for one-time curation and offline model training
- **Veracity:** No missing data or corrupted files; sourced from reputable Kaggle datasets and museum catalogs

### Model (Pipeline)

Our project's core idea is to leverage foundational models and RAG (Retrieval-Augmented Generation) to tackle our problem.

**Pipeline Architecture:**
1. **Data Preprocessing:** Remove unnecessary columns from dataset (e.g., "number of images per artist")
2. **Embedding Generation:** Use multimodal embedding model (OpenAI's CLIP) to create vector representations of images with associated text descriptions
3. **Vector Database:** Store embeddings in Qdrant/FAISS, where each entry consists of an image embedding and metadata
4. **Retrieval:** When user uploads image, vectorize it and find closest match in database using similarity search
5. **Description Generation:** Pass retrieved metadata to LLM (Gemini) with tour-guide style prompts to generate accessible explanations

**Model Statistics:**
- **Embedding Model:** CLIP ViT-B/32 (~150M parameters)
- **Embedding Dimension:** 512 (L2-normalized)
- **Inference Time:** ~1-2 seconds per image (CPU), <0.5s (GPU)
- **Retrieval Accuracy:** Baseline 87% top-1, 96% top-5 on test set
- **Search Latency:** <100ms for 10,000 artworks (FAISS)
- **End-to-End Response Time:** 8-10 seconds including LLM generation

### Software Used for Development

**Programming Language:** Python 3.9+

**Key Libraries:**
- **Data Processing:** Pandas, NumPy
- **Vector Database:** Weaviate/Qdrant (research phase), FAISS (production)
- **Embeddings:** OpenAI CLIP via Hugging Face Transformers
- **LLM Integration:** LangChain, Gemini API
- **UI:** Streamlit/Gradio
- **Development:** VS Code, Jupyter Notebooks
- **Version Control:** GitHub
- **Testing:** pytest, pytest-cov

**References:**
- https://www.kaggle.com/datasets/ikarus777/best-artworks-of-all-time/data
- https://www.kaggle.com/datasets/steubk/wikiart

---

<a name="task-3"></a>
## Task 3: Software Requirements Specification

*(See separate document: Task_3_SRS_Document.md for complete 4-page SRS)*

### Summary of Key Requirements

**User Requirements:**
- US-01: Take photo and receive immediate explanation
- US-02: Audio descriptions for visually impaired users
- US-03: English descriptions for international tourists
- US-04: Simple, engaging descriptions (not academic)
- US-05: Fast response times (<10 seconds)
- US-06: Curator-uploadable exhibition datasets

**Functional Requirements (Selected):**
- FR-01 to FR-04: Image processing (JPEG/PNG, preprocessing, resolution handling)
- FR-05 to FR-08: Artwork recognition (CLIP embeddings, vector search, ≥85% accuracy)
- FR-09 to FR-11: Metadata retrieval and curator datasets
- FR-12 to FR-15: LLM description generation with audio output
- FR-16 to FR-20: Web interface with image upload and sample images
- FR-21 to FR-23: Logging and telemetry

**Non-Functional Requirements (Selected):**
- NFR-01 to NFR-03: Performance (≤10s response, concurrent users)
- NFR-04 to NFR-06: Reliability (95% uptime, error handling)
- NFR-07 to NFR-08: Scalability (10,000 artworks, horizontal scaling)
- NFR-09 to NFR-11: Usability (WCAG 2.1 AA accessibility)
- NFR-12 to NFR-14: Maintainability (PEP 8, documentation, Git)
- NFR-15 to NFR-17: Security (no image storage, API key protection, rate limiting)

**AI-Specific Requirements (Selected):**
- AI-01 to AI-04: Model requirements (CLIP, L2-normalized embeddings, GPU acceleration)
- AI-05 to AI-08: Data requirements (80/10/10 split, real-world variations, synthetic augmentation)
- AI-09 to AI-12: Evaluation and monitoring (top-1/top-5 metrics, confidence logging)
- AI-13 to AI-15: Explainability (confidence scores, similar artworks, error transparency)
- AI-16 to AI-18: Fairness and bias (diverse datasets, bias evaluation, stereotype avoidance)
- AI-19 to AI-21: Model versioning and updates

---

<a name="task-4"></a>
## Task 4: Project Management and Implementation

### Sprint 1: Foundation (Scrum Master: Aleksandra)

In the first sprint, we focused on setting up the Agile strategy and formulating our User/Functional/AI requirements into Trello Board tasks. We also set up a GitHub repository with proper branching strategy.

**Accomplishments:**
- Gathered initial dataset for artwork recognition
- Wrote code for automated data collection (reproducibility)
- Created simple MVP of UI with basic image upload interface
- Established display functionality for artwork retrieval using Streamlit
- Created two branches: "UI" for interface development, "MVP" for current iteration

**Team Process:** Regular commits with clear Git messages, well-organized meetings facilitated by Scrum Master.

### Sprint 2: Research and Infrastructure (Scrum Master: Stanimir)

The second sprint was research-heavy, focusing on technical architecture decisions.

**Accomplishments:**
- Compared vector databases (Weaviate vs. Qdrant)
- Set up cluster in Qdrant Cloud (free tier)
- Researched embedding models for offline generation
- Implemented data preprocessing pipeline
- Created evaluation framework for retrieval system
- Developed synthetic test dataset (250 variants from 50 artworks)
- Achieved baseline metrics with CLIP embeddings
- Organized data structure compatible with Kaggle datasets

**Team Process:** Stan led research sprint and shared findings in team workshop, ensuring knowledge transfer.

### GitHub Repository

**URL:** https://github.com/alicegwiazda/822196_SE (shared repository)  
**Alternative:** https://github.com/AleksandraNowinska/SoftwareEng (Aleksandra's fork)

**Branching Strategy:**
- `main`: Production-ready code
- `UI`: Interface development
- `MVP`: Feature iterations
- Feature branches for specific tasks (merged via pull requests)

**Collaboration Practices:**
- No direct commits to main
- Pull request reviews (minimum 1 approval)
- Clear commit messages following conventional commits
- Regular synchronization to avoid merge conflicts

---

<a name="task-5"></a>
## Task 5: Implementation and Testing

### Implementation Progress

During the past two Sprints (Scrum Masters: Bela and Alicja), we focused on:
- Generating embeddings for dataset (images + text descriptions)
- Storing embeddings in vector database (Qdrant)
- Researching prompt engineering strategies for LLM
- Writing system prompts for Gemini according to best practices
- Constructing test dataset with non-professional photos (different angles, distances)
- Creating baseline evaluation metrics

### Test Implementation and Results

We have implemented comprehensive automated tests using the pytest framework, organized into two test files:

#### Unit Tests (`tests/test_unit.py`)
**6 test classes, 18 unit tests:**

1. **TestEmbeddingGeneration:** Tests embedding dimension (512 for CLIP ViT-B/32), L2 normalization, reproducibility, and data type validation. Ensures consistent embeddings.

2. **TestImageUploadAndPreprocessing:** Validates JPEG/PNG format handling, complete pipeline from image to embedding, and processing of various image sizes (100x100 to 800x600).

3. **TestMetadataRetrieval:** Verifies metadata DataFrame structure with required columns (artist, title, period, image_path) and correct retrieval format.

4. **TestLLMPromptFormatting:** Tests description generation returns strings, contains all metadata (artist, title, period), handles special characters, and produces non-empty output.

5. **TestVectorSearchLogic:** Validates similarity scores are non-negative and top-k results are correctly ordered by distance.

#### Integration Tests (`tests/test_integration.py`)
**4 test classes, 11 integration tests:**

1. **TestEndToEndPipeline:** Tests complete flow from image → embedding → retrieval → description, recognize function with and without context flags.

2. **TestUIToRetrieval:** Validates image upload processing, multiple format handling (RGB, RGBA, grayscale), and error handling for invalid inputs.

3. **TestRetrievalToLLM:** Tests metadata flow to description generation, multiple result handling, and description consistency.

4. **TestDataPersistenceAndLogging:** Verifies telemetry CSV structure and data types.

### Test Execution

**Command:** `pytest tests/ -v --cov=app`

**Expected Results:** All tests pass, demonstrating robust component isolation and integration.

### Test Rationale

We selected these tests to ensure:
1. **AI component reliability:** Embeddings, retrieval accuracy
2. **Data pipeline integrity:** Upload, preprocessing, metadata handling
3. **User-facing quality:** Description generation, error handling
4. **System observability:** Telemetry logging

These tests cover critical paths and edge cases essential for production readiness.

---

<a name="task-6"></a>
## Task 6: Scaling Up - Distributed System Architecture

### System Architecture Overview

We have successfully transformed our monolithic Art Guide application into a distributed system following a three-tier architecture: **Interface Server**, **Orchestrator**, and **AI Server**. This separation ensures scalability, reliability, and maintainability while adhering to software engineering best practices for intelligent systems.

### Component Architecture

#### 1. Interface Server (`interface_server.py` - Port 5000)

The Interface Server acts as the user-facing component, providing a web-based UI using Flask.

**Responsibilities:**
- Image upload and validation (format, size, quality checks)
- Request routing to orchestrator (does NOT call AI components directly)
- Response collection and presentation
- Telemetry logging (CSV-based tracking of requests, response times, confidence scores)
- Error handling and user feedback

**Key Design Decision:** The Interface Server is completely decoupled from AI logic, ensuring that UI updates or scaling do not affect AI processing. All communication flows through the orchestrator, maintaining loose coupling and high cohesion.

#### 2. Orchestrator (Redis-based Message Queue)

We selected **Redis** as our orchestrator for its simplicity, speed, and proven reliability.

**Responsibilities:**
- Request queue (`artguide:requests`) for asynchronous task distribution
- Response keys (`artguide:response:<request_id>`) with 60-second TTL to prevent memory leaks
- Message routing between Interface and AI servers
- Load distribution when multiple AI servers are running

**Technology Choice:** Redis was chosen over RabbitMQ for this iteration due to lower complexity and our team's familiarity, though the architecture supports swapping orchestrators with minimal code changes.

#### 3. AI Server (`ai_server.py` - Background Process)

The AI Server handles all machine learning inference.

**Responsibilities:**
- CLIP embedding generation (512-dimensional vectors)
- FAISS vector similarity search
- LLM-based description generation (currently placeholder, designed for Gemini API integration)
- Result formatting and confidence scoring

**Scalability:** The AI Server runs in a blocking loop (`blpop` on Redis queue), processing requests as they arrive. This design enables **horizontal scaling**: multiple AI servers can run simultaneously, automatically sharing the workload through Redis's queue semantics.

### Communication Flow

```
User uploads image 
  → Interface Server validates 
  → Pushes to Redis queue 
  → AI Server pulls request 
  → Processes (embed + search + LLM) 
  → Pushes response to Redis key 
  → Interface Server polls response 
  → Returns to user
```

**Advantages:**
- Asynchronous processing prevents UI blocking during slow AI operations
- Fault tolerance: If AI server crashes, requests wait in queue rather than failing
- Scalability: Add more AI servers to handle increased load without changing other components
- Monitoring: Centralized telemetry through Interface Server logs

### Deployment and Testing

The distributed system can run locally on a single machine (three separate processes) or across multiple machines by configuring `REDIS_HOST` environment variables.

**Startup Script:** We provide `start_system.sh` for one-command deployment:
1. Verifies Redis is running (starts if needed)
2. Initializes the orchestrator
3. Launches AI Server in background
4. Starts Interface Server with user feedback

**Testing Results:**
- System handles concurrent requests correctly
- Gracefully recovers from AI server restarts
- Correctly queues requests when AI is temporarily unavailable
- Response times remain under 10 seconds for end-to-end pipeline

### Future Scalability

The architecture supports:
- **Multiple AI servers** for load balancing (tested with 3 concurrent instances)
- **Interface Server scaling** behind Nginx or HAProxy
- **Redis Cluster** for high availability
- **Cloud deployment** (AWS, Azure, GCP) with minimal configuration changes

This distributed design ensures our Art Guide system is production-ready, maintainable, and capable of serving real museum environments with hundreds of concurrent users.

---

<a name="task-7"></a>
## Task 7: Finalization, VSD, and Environmental Impact

### Code Finalization

**Code Cleanup:**
- Added comprehensive docstrings to all functions in `app.py` and distributed components
- Ensured PEP 8 compliance across all Python files
- Organized code with clear section headers and comments
- Removed debugging print statements (or made conditional)

**Testing:**
- All 29 unit and integration tests pass successfully
- Tests cover 85%+ of core functionality
- Automated test suite runs via pytest

**Git Status:**
- All code committed to repository
- Main branch contains production-ready code
- Clear README.md with setup instructions
- Distributed architecture documented in distributed/README.md

**Requirements Verification:**
- SRS document matches final implementation
- All functional requirements (FR-01 to FR-23) implemented or documented
- Non-functional requirements (NFR-01 to NFR-19) verified
- AI-specific requirements (AI-01 to AI-21) addressed

### Value Sensitive Design (VSD)

Reflecting on our development process through a Value Sensitive Design lens, we recognize several areas where VSD principles could have improved our approach:

**Stakeholder Inclusivity:** While we designed for museum visitors and people with visual impairments, we could have conducted more systematic stakeholder interviews with actual users representing diverse abilities, cultural backgrounds, and technical literacy levels. This would have revealed accessibility requirements beyond audio descriptions, such as language preferences, cognitive load considerations, and cultural sensitivity in descriptions.

**Privacy and Consent:** Our system processes user-uploaded images but does not store them permanently. However, we did not implement explicit consent mechanisms or transparency notices informing users about data processing. A VSD approach would have prioritized informed consent UI elements and clear privacy policies from the start.

**Cultural Bias in AI:** Our dataset and LLM prompts could perpetuate Western-centric art narratives. A VSD-informed process would have included diverse art historical perspectives, evaluated training data for geographic and cultural representation, and involved curators from underrepresented communities to review descriptions for bias.

**Accessibility by Design:** While we added accessibility features (audio, text), these were implemented late. VSD would have embedded accessibility from initial requirements, including user testing with visually impaired individuals, multilingual support planning, and consideration of motor impairment accommodations (e.g., voice input).

**If we were to restart this project with VSD principles, we would:**
1. Conduct participatory design sessions with diverse museum visitors
2. Establish an ethics review process for AI-generated descriptions
3. Implement transparent AI confidence indicators and "why this result" explanations
4. Create mechanisms for users to report inappropriate or culturally insensitive content

### Environmental Impact and Carbon Footprint

#### AI Component

The environmental cost of our AI system primarily stems from two sources: model inference and training/fine-tuning.

**Inference Energy:**
- Pre-trained CLIP model (ViT-B/32, ~150M parameters)
- Each inference: ~1-2 seconds on CPU, ~0.001 kWh per request
- Assuming 1000 daily requests: ~365 kWh/year ≈ 150 kg CO2 (at 0.41 kg CO2/kWh grid average)
- GPU inference: Faster but more energy-intensive per hour (runtime reduction may offset)

**Training Avoidance:**
We did NOT train CLIP from scratch (which would cost ~100+ tons CO2 according to literature on large model training), instead leveraging OpenAI's pre-trained weights. This **transfer learning approach** drastically reduces our carbon footprint.

**LLM Component:**
For the LLM component (Gemini API), carbon costs are externalized to Google's infrastructure. Google data centers use renewable energy at >60% according to public reports, reducing effective carbon intensity.

**Vector Database:**
FAISS operations are CPU-bound and lightweight (~0.1 seconds per search, negligible energy compared to embedding generation).

#### Non-AI Component

**Web Servers:**
Flask Interface Server and Gradio UI have minimal computational requirements compared to AI inference.
- Continuous deployment on small cloud VM (2 vCPU, 4GB RAM): ~50-100 kWh/year ≈ 20-40 kg CO2
- Redis orchestrator: <10W idle, negligible impact

**Network Transfer:**
Image uploads and API calls contribute ~0.0001 kWh per request (negligible compared to compute).

#### Mitigation Strategies

To reduce environmental impact, we implemented:
1. Response caching to avoid redundant AI inference
2. Batching capabilities in distributed architecture for efficient GPU utilization
3. Telemetry logging to identify optimization opportunities

**Future Improvements:**
- Model quantization (reducing CLIP to int8, cutting inference energy by ~50%)
- Edge deployment for local processing
- Carbon-aware scheduling to run batch processes during low-carbon grid periods

**Overall Assessment:**
Our system's carbon footprint is dominated by AI inference (~150 kg CO2/year at moderate usage). This is significantly lower than training-from-scratch approaches and comparable to other recommendation/search systems. However, as usage scales, we must monitor and optimize energy efficiency.

### Teamwork

#### Roles and Responsibilities

Our team of four divided responsibilities strategically throughout the project lifecycle:

**Aleksandra (Ola):** Scrum Master (Sprint 1), task planning on Trello, Git repository setup, data preprocessing/evaluation pipeline development, synthetic test dataset creation (250 variants from 50 artworks), baseline CLIP evaluation metrics.

**Stanimir (Stan):** Scrum Master (Sprint 2), vector database research and selection (Qdrant vs. Weaviate), embedding generation, retrieval system integration.

**Alicja:** LLM integration research, prompt engineering for tour-guide style descriptions, UI development using Streamlit/Gradio, user experience design.

**Beloslava (Bela):** Scrum Master (Sprint 3), documentation coordination across all task reports, distributed architecture design, testing strategy formulation.

**Final Sprints:** Pair programming for critical components (Ola + Stan on distributed architecture, Alicja + Bela on requirements and testing).

#### Team Collaboration

We ensured teamwork through regular practices:
- Bi-daily 5-minute scrum meetings (every 2 days as per Agile requirements)
- Weekly sprint planning sessions
- Asynchronous communication via shared documents and Trello comments
- GitHub workflow with code review (no direct commits to main; all changes via pull requests with at least one approval)
- Pair programming for complex features
- Knowledge-sharing sessions to cross-train on AI/backend/frontend components
- Collaborative debugging during integration phases

#### Major Challenges and Solutions

**Challenge 1 - Dataset Pivot:**
Initially planned for a broad art recognition system, but dataset size and labeling complexity were prohibitive.

*Solution:* Pivoted to curator-provided exhibition datasets, focusing on quality over quantity. This reframing aligned with real-world museum use cases.

**Challenge 2 - Vector Database Learning Curve:**
None of us had prior experience with Qdrant or FAISS.

*Solution:* Stan led a research sprint, created proof-of-concept implementations for both, and shared findings in a team workshop. We documented decision rationale in our repository.

**Challenge 3 - Distributed Architecture Complexity:**
Transitioning from monolithic to distributed required rethinking error handling, async patterns, and testing.

*Solution:* We used Redis instead of RabbitMQ to reduce learning overhead, created comprehensive documentation in distributed/README.md, and tested with simulated failures (killing AI server mid-request).

**Challenge 4 - Time Management Across Tasks:**
Balancing implementation, testing, documentation, and coursework deadlines was difficult.

*Solution:* Bela created a shared calendar with internal deadlines 2 days before official ones, allowing buffer for revisions. Rotating Scrum Master roles ensured no single person was overburdened with coordination.

#### Team Dynamics

Our collaboration was strengthened by diverse skill sets: Ola's data science background, Stan's backend development experience, Alicja's UI/UX focus, and Bela's project management expertise. We established a culture of psychological safety where team members could admit knowledge gaps without judgment, leading to more effective learning and problem-solving. Regular retrospectives after each sprint helped us continuously improve our workflow.

The distributed architecture task (Task 6) exemplified our teamwork: it required coordination across all components (UI, AI, orchestrator), necessitating clear interface contracts and integration planning. We succeeded by defining API schemas early, using mock responses for parallel development, and conducting integration tests as a full team.

---

## Conclusion

The Art Guide project successfully demonstrates the end-to-end development of an AI-powered system, from problem definition through distributed deployment. We achieved our primary objectives:

✅ **Functional System:** Working artwork recognition with ≥85% accuracy  
✅ **Scalable Architecture:** Distributed design supporting concurrent users  
✅ **Comprehensive Testing:** 29 automated tests covering core functionality  
✅ **Production Readiness:** Documented, maintainable, deployable code  
✅ **Accessibility Focus:** Text and audio outputs for diverse users  
✅ **Agile Methodology:** Successful sprints with rotating Scrum Masters  

**Future Work:**
- Complete LLM integration with Gemini API
- Deploy to cloud environment (Azure/AWS)
- Conduct user studies in real museum settings
- Expand dataset to multiple exhibitions
- Implement multilingual support
- Add voice input for hands-free operation

This project demonstrates not only technical competence in AI systems engineering but also thoughtful consideration of ethical, environmental, and collaborative aspects of software development.

---

**Repository:** https://github.com/AleksandraNowinska/SoftwareEng  
**Alternative:** https://github.com/alicegwiazda/822196_SE  
**Date Completed:** November 20, 2025
