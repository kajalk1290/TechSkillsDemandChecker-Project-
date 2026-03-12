#!/bin/bash

echo "========================================"
echo "Tech Skills Demand Checker"
echo "========================================"
echo ""

echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python not found! Please install Python first."
    exit 1
fi

python3 --version
echo ""

echo "Installing dependencies..."
pip3 install -r requirements.txt

echo ""
echo "========================================"
echo "Select mode:"
echo "1. Command Line Version"
echo "2. Web Application"
echo "========================================"
echo ""

read -p "Enter your choice (1 or 2): " choice

if [ "$choice" == "1" ]; then
    echo ""
    echo "Starting Command Line Version..."
    python3 tech_skills_scraper.py
elif [ "$choice" == "2" ]; then
    echo ""
    echo "Starting Web Application..."
    echo "Open browser and go to: http://localhost:5000"
    python3 app.py
else
    echo "Invalid choice!"
    exit 1
fi
