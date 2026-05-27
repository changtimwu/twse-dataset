#!/bin/bash
# TWSE Fetcher Skill Installation Script

set -e

SKILL_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "TWSE Fetcher Skill Installation"
echo "================================"
echo "Skill directory: $SKILL_DIR"
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -q -r "$SKILL_DIR/requirements.txt"
echo "✓ Dependencies installed"

# Make scripts executable
chmod +x "$SKILL_DIR/fetch_twse_stocks.py"
chmod +x "$SKILL_DIR/fetch_all_twse_modes.py"
echo "✓ Scripts are executable"

echo ""
echo "Installation complete!"
echo ""
echo "Quick start:"
echo "  cd $SKILL_DIR"
echo "  python3 fetch_twse_stocks.py 'https://isin.twse.com.tw/isin/C_public.jsp?strMode=2'"
echo ""
echo "Or fetch all modes:"
echo "  python3 fetch_all_twse_modes.py"
echo ""
echo "See QUICKSTART.md for more examples."
