#!/bin/bash

# Local Development Server for AAS API Documentation
# This script starts a local web server from the repository root

echo "=========================================="
echo "  AAS API Documentation - Local Server"
echo "=========================================="
echo ""

# Check if we're in the repository root
if [ ! -d "docs" ]; then
    echo "❌ Error: docs/ folder not found"
    echo "   Please run this script from the repository root"
    exit 1
fi

# Get the port (default to 8000)
PORT=${1:-8000}

echo "✅ Starting server on port $PORT..."
echo ""
echo "📂 Serving from: $(pwd)"
echo "🌐 Documentation: http://localhost:$PORT/docs/"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=========================================="
echo ""

# Start Python HTTP server
python3 -m http.server $PORT
