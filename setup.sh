#!/bin/bash

# Personal In and Out Dashboard - Setup Script
# Creates virtual environment and installs dependencies

set -e

echo "📊 Personal In and Out Dashboard - Setup"
echo "=========================================="

# Check Python version
python_version=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python 3.8 or higher is required. Found: $python_version"
    exit 1
fi

echo "✅ Python version check passed: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment and install dependencies
echo "📦 Installing dependencies in virtual environment..."
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "🚀 To start the dashboard, run:"
echo "   source venv/bin/activate"
echo "   python3 start_dashboard.py"
echo ""
echo "💰 Features available:"
echo "   • South African Rand (ZAR) currency support"
echo "   • Bank statement import and processing"
echo "   • Budget management per entity"
echo "   • South African tax reporting"
echo "   • CLI dashboard with 9 menu options"
echo "   • Complete standalone deployment"
echo ""
echo "📊 Your Personal In and Out Dashboard is ready!"