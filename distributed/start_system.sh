#!/bin/bash

# Start script for Art Guide Distributed System

echo "🎨 Starting Art Guide Distributed System"
echo "========================================"

# Check if Redis is running
if ! redis-cli ping > /dev/null 2>&1; then
    echo "❌ Redis is not running. Starting Redis..."
    
    # Try to start Redis based on OS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        brew services start redis 2>/dev/null || redis-server --daemonize yes
    else
        # Linux
        sudo systemctl start redis 2>/dev/null || redis-server --daemonize yes
    fi
    
    sleep 2
    
    if ! redis-cli ping > /dev/null 2>&1; then
        echo "❌ Failed to start Redis. Please start it manually:"
        echo "   macOS: brew services start redis"
        echo "   Linux: sudo systemctl start redis"
        echo "   Docker: docker run -d -p 6379:6379 redis:alpine"
        exit 1
    fi
fi

echo "✓ Redis is running"

# Setup orchestrator
echo ""
echo "Setting up orchestrator (initial setup)..."
python distributed/orchestrator.py

# Start Orchestrator Service in background
echo ""
echo "Starting Orchestrator Service..."
python distributed/orchestrator_service.py &
ORCHESTRATOR_PID=$!
echo "✓ Orchestrator Service started (PID: $ORCHESTRATOR_PID)"

# Start AI Server in background
echo ""
echo "Starting AI Server..."
python distributed/ai_server.py &
AI_SERVER_PID=$!
echo "✓ AI Server started (PID: $AI_SERVER_PID)"

# Wait a moment for servers to initialize
sleep 3

# Start Interface Server
echo ""
echo "Starting Interface Server..."
echo "========================================"
echo "🌐 Web Interface: http://localhost:5000"
echo "🤖 AI Server: Running in background (PID: $AI_SERVER_PID)"
echo "📊 Orchestrator Service: Running in background (PID: $ORCHESTRATOR_PID)"
echo "🗄️  Redis Queue: localhost:6379"
echo "========================================"
echo "Press Ctrl+C to stop all services"
echo ""

python distributed/interface_server.py

# Cleanup on exit
echo ""
echo "Shutting down all services..."
kill $AI_SERVER_PID 2>/dev/null
kill $ORCHESTRATOR_PID 2>/dev/null
echo "✓ All services stopped"
