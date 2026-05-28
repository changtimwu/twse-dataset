#!/bin/bash
# TWSE Fetcher Skill Installer
# Installs the skill to ~/.claude/skills/twse-fetch/
# Usage: bash install-skill.sh

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔══════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  TWSE Fetcher Skill Installer        ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════╝${NC}"
echo ""

SKILL_DIR="$HOME/.claude/skills/twse-fetch"
REPO_URL="https://github.com/changtimwu/twse-dataset.git"

# Check if already installed
if [ -d "$SKILL_DIR" ]; then
    echo -e "${YELLOW}⚠ Skill already exists at: $SKILL_DIR${NC}"
    read -p "Overwrite? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Installation cancelled."
        exit 0
    fi
    rm -rf "$SKILL_DIR"
fi

# Create skills directory if it doesn't exist
mkdir -p "$(dirname "$SKILL_DIR")"

echo -e "${BLUE}Installing to: $SKILL_DIR${NC}"
echo ""

# Clone or copy the skill files
if command -v git &> /dev/null; then
    echo "Cloning from GitHub..."
    git clone --depth 1 "$REPO_URL" "$SKILL_DIR" 2>/dev/null || {
        echo -e "${YELLOW}Git clone failed, using direct copy...${NC}"
        mkdir -p "$SKILL_DIR"
        for file in fetch_twse_stocks.py fetch_all_twse_modes.py fetch_company_profile.py refresh_company_profiles.py query_companies.py company_profiles.jsonl SKILL.md QUICKSTART.md requirements.txt install.sh; do
            if [ -f "$file" ]; then
                cp "$file" "$SKILL_DIR/"
            fi
        done
    }
else
    echo "Copying files locally..."
    mkdir -p "$SKILL_DIR"
    for file in fetch_twse_stocks.py fetch_all_twse_modes.py fetch_company_profile.py refresh_company_profiles.py query_companies.py company_profiles.jsonl SKILL.md QUICKSTART.md requirements.txt install.sh; do
        if [ -f "$file" ]; then
            cp "$file" "$SKILL_DIR/"
        fi
    done
fi

# Make scripts executable
chmod +x "$SKILL_DIR"/*.py "$SKILL_DIR"/*.sh 2>/dev/null || true

# Install dependencies
echo ""
echo -e "${BLUE}Installing Python dependencies...${NC}"
if [ -f "$SKILL_DIR/requirements.txt" ]; then
    pip install -q -r "$SKILL_DIR/requirements.txt"
    echo -e "${GREEN}✓ Dependencies installed${NC}"
fi

# Verify installation
echo ""
echo -e "${BLUE}Verifying installation...${NC}"

if [ -f "$SKILL_DIR/fetch_twse_stocks.py" ]; then
    echo -e "${GREEN}✓ Skill files installed${NC}"
else
    echo -e "${YELLOW}✗ Installation may have failed${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}╔══════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  Installation Complete!              ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}Quick Start:${NC}"
echo "  python3 ~/.claude/skills/twse-fetch/fetch_twse_stocks.py \\"
echo "    \"https://isin.twse.com.tw/isin/C_public.jsp?strMode=2\""
echo ""
echo -e "${BLUE}Or fetch all modes:${NC}"
echo "  cd ~/.claude/skills/twse-fetch && python3 fetch_all_twse_modes.py"
echo ""
echo -e "${BLUE}Documentation:${NC}"
echo "  cat ~/.claude/skills/twse-fetch/QUICKSTART.md"
echo ""
