# Distributed System Architecture - Art Guide

This directory contains the distributed implementation of the Art Guide system, fully compliant with Task 6 requirements. The system is separated into three independent servers:

1. **Interface Server** (`interface_server.py`) - Port 5000
2. **Orchestrator Service** (`orchestrator_service.py`) - Monitoring service using Redis (Port 6379)
3. **AI Server** (`ai_server.py`) - Background AI inference process

## Architecture (Task 6 Compliant)

```
User → Interface Server → Orchestrator Service (Redis Queue) → AI Server
                ↓                    ↓                              ↓
            Validation           Queue                      AI Processing
            Logging          Management                (CLIP + Vector Search)
                ↓             Monitoring                          ↓
            Response ←    Response Routing     ←          Result Published
```

**Key Requirements from Task 6:**
✅ "One server that provides the interface" - Interface Server  
✅ "One or more servers to contain the AI component" - AI Server  
✅ "One or more servers to host the orchestrator" - Orchestrator Service  
✅ "Interface should NOT call AI directly" - Routes through Redis queue  
✅ "Can use queue services like RabbitMQ" - Uses Redis as message broker

## Components

### Interface Server
- **Role:** User-facing web interface
- **Responsibilities:**
  - Accept image uploads
  - Validate input (format, size, quality)
  - Send requests to orchestrator
  - Wait for AI server response
  - Log telemetry
  - Display results to user
- **Does NOT:** Call AI components directly
- **Port:** 5000

### AI Server
- **Role:** AI inference engine
- **Responsibilities:**
  - Listen to orchestrator queue
  - Generate CLIP embeddings
  - Perform vector similarity search
  - Generate descriptions (LLM integration)
  - Send results back via orchestrator
- **Does NOT:** Handle user requests directly

### Orchestrator Service
- **Role:** Message broker coordinator and system monitor
- **Technology:** Python service wrapping Redis queue infrastructure
- **Responsibilities:**
  - Manage Redis queue (artguide:requests)
  - Route requests from Interface Server to AI Server
  - Monitor request/response flow in real-time
  - Track system metrics and performance
  - Handle graceful shutdown
  - Provide load balancing (when multiple AI servers)
- **Does NOT:** Process images or make AI inferences
- **Queue Infrastructure:** Redis (Port 6379)
- **Service Port:** 6380 (monitoring)

## Setup

### Prerequisites
```bash
# Install Redis
# macOS:
brew install redis
brew services start redis

# Linux:
sudo apt-get install redis-server
sudo systemctl start redis

# Docker:
docker run -d -p 6379:6379 redis:alpine

# Install Python dependencies
pip install -r requirements.txt
pip install flask redis
```

### Running the System

**Option 1: Using the start script (recommended)**
```bash
chmod +x distributed/start_system.sh
./distributed/start_system.sh
```

**Option 2: Manual startup (for debugging/development)**
```bash
# Terminal 1: Setup Redis queue structures
python distributed/orchestrator.py

# Terminal 2: Start Orchestrator Service
python distributed/orchestrator_service.py

# Terminal 3: Start AI server
python distributed/ai_server.py

# Terminal 4: Start interface server
python distributed/interface_server.py

# Access at http://localhost:5000
```

## Testing the Distributed System

```bash
# Health check
curl http://localhost:5000/health

# Upload image
curl -X POST -F "image=@path/to/artwork.jpg" http://localhost:5000/api/recognize
```

## Monitoring

```bash
# Monitor the orchestrator (shows real-time queue stats)
# The orchestrator service automatically monitors when running

# Check Redis directly
redis-cli monitor

# View orchestrator metrics
redis-cli hgetall artguide:metrics

# Monitor queue manually
python distributed/orchestrator.py monitor
```

## Configuration

Environment variables:
- `REDIS_HOST` - Redis hostname (default: localhost)
- `REDIS_PORT` - Redis port (default: 6379)
- `INDEX_PATH` - FAISS index path (default: models/faiss.index)
- `META_PATH` - Metadata path (default: models/metadata.parquet)

## Scaling

### Horizontal Scaling
- **AI Servers:** Run multiple instances of `ai_server.py` - they will automatically share the queue
- **Interface Servers:** Run behind a load balancer (Nginx, HAProxy)
- **Orchestrator:** Use Redis Cluster for high availability

### Example: Multiple AI Servers
```bash
# Terminal 1
python distributed/ai_server.py

# Terminal 2
python distributed/ai_server.py

# Terminal 3
python distributed/ai_server.py
# All three will process requests from the same queue
```

## Advantages of This Architecture

1. **Separation of Concerns:** UI logic separated from AI inference
2. **Scalability:** Add more AI servers to handle load
3. **Reliability:** If AI server crashes, requests queue up and wait
4. **Monitoring:** Centralized logging and telemetry
5. **Flexibility:** Easy to swap Redis for RabbitMQ or Kafka
6. **Testing:** Components can be tested independently

## Future Enhancements

- Add RabbitMQ as alternative orchestrator
- Implement load balancing for multiple AI servers
- Add monitoring dashboard (Grafana + Prometheus)
- Implement request prioritization
- Add caching layer for frequent queries
