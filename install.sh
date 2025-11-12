#!/bin/bash

# Personal In and Out Dashboard - Standalone Installer

set -e

echo "📊 Personal In and Out Dashboard - Installer"
echo "=========================================="

# Check Python version
python_version=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python 3.8 or higher is required. Found: $python_version"
    exit 1
fi

echo "✅ Python version check passed: $python_version"

# Install dependencies
echo "📦 Installing financial dashboard dependencies..."
pip3 install -r requirements.txt

echo ""
echo "🎉 Installation completed successfully!"
echo ""
echo "🚀 To start the dashboard, run:"
echo "   python3 start_dashboard.py"
echo ""
echo "💰 Features available:"
echo "   • South African Rand (ZAR) currency support"
echo "   • Bank statement import and processing"
echo "   • Budget management per entity"
echo "   • South African tax reporting"
echo "   • CLI dashboard with 9 menu options"
echo "   • Complete deployment package"
echo ""
echo "📊 Your Personal In and Out Dashboard is ready!"