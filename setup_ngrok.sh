#!/bin/bash

# Ngrok Setup for The Riddle Room Beta Page
# This script will make your beta signup page accessible from anywhere on the web

echo "🌍 Setting up ngrok for The Riddle Room Beta Page"
echo "=================================================="

# Check if FastAPI server is running
if ! pgrep -f "uvicorn.*main:app" > /dev/null; then
    echo "❌ FastAPI server is not running!"
    echo "Please start your server first with:"
    echo "cd /home/m/crypticmessages && source .venv/bin/activate && uvicorn main:app --reload --host 0.0.0.0 --port 8000"
    exit 1
fi

echo "✅ FastAPI server is running"

# Check if port 8000 is accessible
if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/beta | grep -q "200"; then
    echo "✅ Beta page is accessible locally"
else
    echo "❌ Beta page is not accessible. Please check your server."
    exit 1
fi

echo ""
echo "🚀 Starting ngrok tunnel..."
echo "This will make your beta page accessible from anywhere on the web!"
echo ""
echo "📝 Instructions:"
echo "1. Keep this terminal window open to maintain the tunnel"
echo "2. Your beta page will be accessible via the ngrok URL shown below"
echo "3. Update your YouTube video description with the ngrok URL"
echo "4. Press Ctrl+C to stop the tunnel when done"
echo ""
echo "🔗 Starting tunnel for localhost:8000..."
echo ""

# Start ngrok tunnel
ngrok http 8000
