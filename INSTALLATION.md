# TWSE Fetcher Skill - Installation Guide

Multiple installation methods are available depending on your preference and setup.

## Method 1: Quick Install Script (Recommended)

The easiest way to install the skill:

```bash
# Download and run the installer
curl -fsSL https://raw.githubusercontent.com/changtimwu/twse-dataset/main/install-skill.sh | bash
```

Or locally:
```bash
bash install-skill.sh
```

This will:
- ✅ Clone the skill to `~/.claude/skills/twse-fetch/`
- ✅ Install Python dependencies
- ✅ Make scripts executable
- ✅ Verify the installation

## Method 2: Manual Installation

If you prefer to install manually:

```bash
# Create skills directory
mkdir -p ~/.claude/skills

# Clone the repository
git clone https://github.com/changtimwu/twse-dataset.git ~/.claude/skills/twse-fetch

# Install dependencies
pip install requests beautifulsoup4

# Make scripts executable
chmod +x ~/.claude/skills/twse-fetch/*.py
```

## Method 3: Copy to Existing Project

If you already have the repository cloned:

```bash
# Option A: Copy scripts to your project
cp fetch_twse_stocks.py fetch_all_twse_modes.py /path/to/your/project/

# Option B: Use from current directory
python3 fetch_twse_stocks.py "https://isin.twse.com.tw/isin/C_public.jsp?strMode=2"
```

## Verification

After installation, verify everything works:

```bash
# Test the skill
python3 ~/.claude/skills/twse-fetch/fetch_twse_stocks.py \
  "https://isin.twse.com.tw/isin/C_public.jsp?strMode=2"

# Should create: twse_listed_stocks.csv
ls -lh twse_*.csv
```

## Installation Details

### What Gets Installed

```
~/.claude/skills/twse-fetch/
├── SKILL.md                    # Full documentation
├── QUICKSTART.md               # Quick start guide
├── fetch_twse_stocks.py        # Single mode fetcher
├── fetch_all_twse_modes.py     # Batch fetcher
├── requirements.txt            # Python dependencies
├── install.sh                  # Individual installer
└── skill-manifest.json         # Skill metadata
```

### Dependencies

- **Python 3.6+** (usually pre-installed)
- **pip** (Python package manager)
- **requests** — HTTP library for fetching web content
- **beautifulsoup4** — HTML parsing library

These are automatically installed by the setup script.

### System Requirements

- Linux, macOS, or Windows (with git/bash)
- ~20 MB disk space
- Internet connection (to fetch from TWSE)

## Troubleshooting

### "Command not found: bash"

Use `sh` instead:
```bash
sh install-skill.sh
```

### "ImportError: No module named 'requests'"

Install dependencies manually:
```bash
pip install requests beautifulsoup4
```

### "Permission denied"

Make scripts executable:
```bash
chmod +x ~/.claude/skills/twse-fetch/*.py
```

### Git not installed

The installer will fall back to copying files directly. Ensure the source files are available.

## Uninstallation

To remove the skill:

```bash
rm -rf ~/.claude/skills/twse-fetch/
```

## Updating

To update to the latest version:

```bash
# Option 1: Reinstall
bash install-skill.sh

# Option 2: Pull latest from git
cd ~/.claude/skills/twse-fetch
git pull
```

## Using the Installed Skill

### Quick fetch
```bash
python3 ~/.claude/skills/twse-fetch/fetch_twse_stocks.py \
  "https://isin.twse.com.tw/isin/C_public.jsp?strMode=2"
```

### Fetch all modes
```bash
cd ~/.claude/skills/twse-fetch
python3 fetch_all_twse_modes.py
```

### Add to PATH for easy access
```bash
export PATH="$PATH:$HOME/.claude/skills/twse-fetch"
fetch_twse_stocks.py "https://isin.twse.com.tw/isin/C_public.jsp?strMode=2"
```

## Documentation

- **Full guide:** `~/.claude/skills/twse-fetch/SKILL.md`
- **Quick start:** `~/.claude/skills/twse-fetch/QUICKSTART.md`
- **This file:** `INSTALLATION.md`

## Support

For issues or questions:
- Check the QUICKSTART.md guide
- Review SKILL.md for detailed documentation
- Open an issue on GitHub: https://github.com/changtimwu/twse-dataset/issues

## Next Steps

After installation, try:

1. **Fetch listed stocks:**
   ```bash
   python3 ~/.claude/skills/twse-fetch/fetch_twse_stocks.py \
     "https://isin.twse.com.tw/isin/C_public.jsp?strMode=2"
   ```

2. **Fetch all data:**
   ```bash
   cd ~/.claude/skills/twse-fetch && python3 fetch_all_twse_modes.py
   ```

3. **Read the quick start:**
   ```bash
   cat ~/.claude/skills/twse-fetch/QUICKSTART.md
   ```
