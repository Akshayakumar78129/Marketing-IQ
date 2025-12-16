#!/bin/bash

echo "Setting up Marketing IQ local environment..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker Desktop."
    exit 1
fi

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "Python is not installed. Please install Python 3.11+."
    exit 1
fi

# Start Docker services
echo "Starting Docker services..."
docker-compose up -d

# Wait for services to be ready
echo "Waiting for services to start..."
sleep 10

# Create Python virtual environment
echo "Creating Python virtual environment..."
python -m venv venv

echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Activate virtual environment:"
echo "   - Windows: .\\venv\\Scripts\\activate"
echo "   - Mac/Linux: source venv/bin/activate"
echo ""
echo "2. Install backend dependencies:"
echo "   cd backend && pip install -r requirements.txt"
echo ""
echo "3. Run API:"
echo "   uvicorn app.main:app --reload"
echo ""
echo "4. Access API docs:"
echo "   http://localhost:8000/api/docs"
