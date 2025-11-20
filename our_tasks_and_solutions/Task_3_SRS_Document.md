# Software Requirements Specification (SRS)
## Art Guide - AI-Powered Artwork Recognition and Description System

**Project:** AlBeSa Art Guide  
**Authors:** Beloslava Malakova, Alicja Gwiazda, Stanimir Dimitrov, Aleksandra Nowińska  
**Version:** 1.0  
**Date:** November 2025

---

## 1. Introduction

### 1.1 Purpose
This Software Requirements Specification (SRS) document describes the functional and non-functional requirements for the Art Guide system, an AI-powered application that enables museum and gallery visitors to obtain immediate, accessible information about artworks through image recognition and natural language descriptions.

### 1.2 Scope
The Art Guide system will:
- Accept user-uploaded photographs of artworks
- Identify artworks using deep learning-based image recognition
- Retrieve contextual metadata from vector databases
- Generate human-readable descriptions using Large Language Models (LLMs)
- Provide both text and audio output for accessibility
- Log user interactions for analytics and system improvement

### 1.3 Intended Audience
- Museum visitors and tourists
- Art enthusiasts with varying levels of expertise
- Individuals with visual impairments requiring audio descriptions
- Museum curators for content management
- System administrators for maintenance and monitoring

---

## 2. User Requirements

### 2.1 User Stories
**US-01:** As a museum visitor, I want to take a photo of an artwork and receive an immediate explanation, so that I can learn about the piece without needing a tour guide.

**US-02:** As a visually impaired user, I want to receive audio descriptions of artworks, so that I can access cultural content independently.

**US-03:** As an international tourist, I want descriptions in English, so that I can understand artworks regardless of the museum's primary language.

**US-04:** As a casual art enthusiast, I want simple, engaging descriptions rather than academic text, so that information is accessible without prior art knowledge.

**US-05:** As a user with limited time, I want fast response times (<10 seconds), so that I can explore multiple artworks during my visit.

**US-06:** As a curator, I want to upload exhibition-specific datasets, so that the system provides accurate information for current exhibitions.

### 2.2 User Characteristics
- **Technical proficiency:** Minimal to moderate (smartphone users)
- **Domain knowledge:** No prior art history knowledge required
- **Accessibility needs:** Support for visual impairments, multilingual tourists
- **Usage context:** On-site in museums/galleries with varying lighting and network conditions

---

## 3. System Requirements

### 3.1 Functional Requirements

#### 3.1.1 Image Processing
**FR-01:** The system SHALL accept image uploads in JPEG and PNG formats.  
**FR-02:** The system SHALL preprocess images to standard dimensions (224x224 pixels) for embedding generation.  
**FR-03:** The system SHALL handle images of varying resolutions (100x100 to 4000x4000 pixels).  
**FR-04:** The system SHALL convert images with different color modes (RGB, RGBA, grayscale) to a standard RGB format.

#### 3.1.2 Artwork Recognition
**FR-05:** The system SHALL generate 512-dimensional embeddings using CLIP (ViT-B/32) model.  
**FR-06:** The system SHALL perform similarity search against a vector database (FAISS/Qdrant) to identify artworks.  
**FR-07:** The system SHALL return top-5 most similar artworks with confidence scores.  
**FR-08:** The system SHALL achieve ≥85% recognition accuracy on test datasets.

#### 3.1.3 Metadata Retrieval
**FR-09:** The system SHALL retrieve metadata including artist name, artwork title, period/style, and creation year.  
**FR-10:** The system SHALL store metadata in structured format (Parquet/CSV) linked to vector embeddings.  
**FR-11:** The system SHALL support curator-uploaded custom datasets for specific exhibitions.

#### 3.1.4 Description Generation
**FR-12:** The system SHALL generate contextual descriptions using an LLM (Gemini API or equivalent).  
**FR-13:** Descriptions SHALL include artist information, historical context, artistic style, and cultural significance.  
**FR-14:** The system SHALL use prompt engineering to ensure descriptions are tour-guide style, accessible, and engaging.  
**FR-15:** The system SHALL provide descriptions in both text and audio formats.

#### 3.1.5 User Interface
**FR-16:** The system SHALL provide a web-based interface accessible via browsers (Gradio/Streamlit).  
**FR-17:** The interface SHALL allow image upload via file selection or camera capture.  
**FR-18:** The interface SHALL display recognition results, confidence scores, and descriptions.  
**FR-19:** The interface SHALL include a toggle for showing/hiding context (similar artworks).  
**FR-20:** The interface SHALL provide sample images for quick demonstration.

#### 3.1.6 Logging and Telemetry
**FR-21:** The system SHALL log each recognition request with timestamp, artist, confidence, and response time.  
**FR-22:** Logs SHALL be stored in CSV format for analytics and performance monitoring.  
**FR-23:** The system SHALL respect user privacy and not store uploaded images permanently.

### 3.2 Non-Functional Requirements

#### 3.2.1 Performance
**NFR-01:** Response time SHALL be ≤10 seconds from image upload to description display (90th percentile).  
**NFR-02:** Embedding generation SHALL complete in ≤2 seconds per image.  
**NFR-03:** The system SHALL support concurrent requests from up to 50 users.

#### 3.2.2 Reliability
**NFR-04:** System uptime SHALL be ≥95% during exhibition hours.  
**NFR-05:** The system SHALL gracefully handle missing or corrupted image files.  
**NFR-06:** The system SHALL provide meaningful error messages for failed recognition attempts.

#### 3.2.3 Scalability
**NFR-07:** The vector database SHALL support up to 10,000 artworks per exhibition.  
**NFR-08:** The system architecture SHALL support horizontal scaling via distributed components.

#### 3.2.4 Usability
**NFR-09:** The interface SHALL be intuitive for users with minimal technical knowledge.  
**NFR-10:** Font sizes and contrast SHALL meet WCAG 2.1 Level AA accessibility standards.  
**NFR-11:** Audio output SHALL use natural, clear text-to-speech synthesis.

#### 3.2.5 Maintainability
**NFR-12:** Code SHALL follow PEP 8 style guidelines for Python.  
**NFR-13:** All modules SHALL include comprehensive docstrings and inline comments.  
**NFR-14:** The system SHALL use version control (Git) with clear commit messages.

#### 3.2.6 Security
**NFR-15:** The system SHALL NOT store user-uploaded images after processing.  
**NFR-16:** API keys for external services (LLM APIs) SHALL be stored securely using environment variables.  
**NFR-17:** The system SHALL implement rate limiting to prevent abuse.

#### 3.2.7 Portability
**NFR-18:** The system SHALL run on Linux, macOS, and Windows environments.  
**NFR-19:** The system SHALL use containerization (Docker) for consistent deployment.

---

## 4. AI-Specific Requirements

### 4.1 Model Requirements
**AI-01:** The image embedding model SHALL use a pre-trained CLIP (openai/clip-vit-base-patch32) architecture.  
**AI-02:** Embeddings SHALL be L2-normalized to enable cosine similarity search.  
**AI-03:** The LLM SHALL be capable of contextual text generation (Gemini 1.5 or GPT-4 equivalent).  
**AI-04:** Model inference SHALL utilize GPU acceleration when available, falling back to CPU.

### 4.2 Data Requirements
**AI-05:** Training/validation data SHALL be split 80/10/10 (train/dev/test).  
**AI-06:** Test datasets SHALL include real-world variations (blur, glare, angles, lighting).  
**AI-07:** The system SHALL use synthetic data augmentation to improve robustness.  
**AI-08:** Dataset SHALL include metadata verification to ensure label accuracy (veracity).

### 4.3 Evaluation and Monitoring
**AI-09:** Recognition accuracy SHALL be evaluated using top-1 and top-5 metrics.  
**AI-10:** The system SHALL log confidence scores for post-deployment analysis.  
**AI-11:** Model performance SHALL be monitored continuously, triggering retraining if accuracy drops below 80%.  
**AI-12:** The system SHALL track retrieval latency and LLM generation time separately.

### 4.4 Explainability and Transparency
**AI-13:** The system SHALL display confidence scores to users for transparency.  
**AI-14:** The system SHALL provide context by showing similar artworks (optional toggle).  
**AI-15:** Error messages SHALL clearly indicate when recognition confidence is low (<70%).

### 4.5 Fairness and Bias
**AI-16:** Training datasets SHALL include diverse artistic styles, periods, and cultural origins.  
**AI-17:** The system SHALL be evaluated for bias across different art movements and artists.  
**AI-18:** LLM prompts SHALL be designed to avoid cultural stereotypes or biased language.

### 4.6 Model Updates and Versioning
**AI-19:** The system SHALL support model versioning to enable rollback in case of performance degradation.  
**AI-20:** Embeddings SHALL be regenerated when the embedding model is updated.  
**AI-21:** The system SHALL maintain backward compatibility for at least one prior model version.

---

## 5. Constraints and Assumptions

### 5.1 Constraints
- Limited to artworks included in the curator-provided dataset
- Requires internet connectivity for LLM API calls
- GPU resources may be limited in deployment environment

### 5.2 Assumptions
- Users have smartphones or devices capable of capturing photos
- Museums provide stable Wi-Fi or cellular connectivity
- Curators provide high-quality, labeled datasets for each exhibition

---

## 6. Appendix

### 6.1 Glossary
- **CLIP:** Contrastive Language-Image Pre-training, a multimodal embedding model
- **FAISS:** Facebook AI Similarity Search, a vector similarity search library
- **LLM:** Large Language Model
- **RAG:** Retrieval-Augmented Generation
- **Embedding:** Dense vector representation of an image or text

### 6.2 References
- OpenAI CLIP: https://github.com/openai/CLIP
- FAISS Documentation: https://github.com/facebookresearch/faiss
- Gemini API: https://ai.google.dev/
- WCAG 2.1 Guidelines: https://www.w3.org/WAI/WCAG21/quickref/
