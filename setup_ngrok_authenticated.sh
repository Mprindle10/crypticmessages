#!/bin/bash

# Quick Ngrok Setup for The Riddle Room
# This script will guide you through the ngrok authentication process

echo "🌍 Ngrok Setup for The Riddle Room Beta Page"
echo "=============================================="
echo ""

# Check if authtoken is configured
if ngrok config check >/dev/null 2>&1; then
    echo "✅ Ngrok is already configured!"
    echo ""
else
    echo "🔑 Ngrok Authentication Required"
    echo ""
    echo "To make your beta page accessible worldwide, you need a free ngrok account:"
    echo ""
    echo "1. 📝 Sign up (FREE): https://dashboard.ngrok.com/signup"
    echo "2. 🔑 Get your token: https://dashboard.ngrok.com/get-started/your-authtoken"
    echo "3. 📋 Copy the authtoken from the dashboard"
    echo ""
    echo -n "4. 🔧 Enter your authtoken here: "
    read -r authtoken
    
    if [ -n "$authtoken" ]; then
        echo ""
        echo "🔧 Configuring ngrok with your authtoken..."
        ngrok config add-authtoken "$authtoken"
        
        if [ $? -eq 0 ]; then
            echo "✅ Ngrok configured successfully!"
            echo ""
        else
            echo "❌ Failed to configure ngrok. Please check your authtoken."
            exit 1
        fi
    else
        echo "❌ No authtoken provided. Please run this script again with your token."
        exit 1
    fi
fi

# Check if FastAPI server is running
if ! pgrep -f "uvicorn.*main:app" > /dev/null; then
    echo "❌ FastAPI server is not running!"
    echo "Please start your server first:"
    echo "cd /home/m/crypticmessages && source .venv/bin/activate && uvicorn main:app --reload --host 0.0.0.0 --port 8000"
    exit 1
fi

echo "✅ FastAPI server is running"

# Check if beta page is accessible
if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/beta | grep -q "200"; then
    echo "✅ Beta page is accessible locally"
else
    echo "❌ Beta page is not accessible. Please check your server."
    exit 1
fi

echo ""
echo "🚀 Starting ngrok tunnel..."
echo ""
echo "📝 Important:"
echo "• Keep this terminal open to maintain the tunnel"
echo "• Your beta page will be accessible worldwide via the ngrok URL"
echo "• Copy the HTTPS URL for your YouTube video description"
echo "• Press Ctrl+C to stop the tunnel"
echo ""
echo "🔗 Creating public tunnel for localhost:8000..."
echo ""

# Start ngrok with better output formatting
ngrok http 8000 --log=stdout --log-level=info
