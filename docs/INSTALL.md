# Tikun Olam - Installation Guide

## Requirements

- Python 3.8 or higher
- API Keys for:
  - Google Gemini (required)
  - Anthropic Claude (required)
  - DeepSeek (required for BinahSigma)
  - OpenAI (optional)

## Installation Steps

### 1. Clone or Download the Repository

```bash
git clone https://github.com/yourusername/tikun-olam.git
cd tikun-olam
```

### 2. Create a Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install the package in development mode:

```bash
pip install -e .
```

### 4. Configure API Keys

#### 4.1 Get API Keys

You'll need to obtain API keys from:

1. **Google Gemini**: https://makersuite.google.com/app/apikey
2. **Anthropic Claude**: https://console.anthropic.com/
3. **DeepSeek**: https://platform.deepseek.com/
4. **OpenAI** (optional): https://platform.openai.com/api-keys

#### 4.2 Create .env File

Copy the example environment file:

```bash
cp .env.example .env
```

Then edit `.env` and add your API keys:

```bash
# Required API Keys
GEMINI_API_KEY=your_gemini_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# Optional
OPENAI_API_KEY=your_openai_api_key_here  # Optional fallback
```

**IMPORTANT**: The `.env` file is git-ignored for security. Never commit API keys to version control.

### 5. Verify Installation

Run a simple test to verify everything is working:

```python
from tikun import TikunOrchestrator

# Create orchestrator
orchestrator = TikunOrchestrator(verbose=True)

# Test scenario
scenario = """
PROPOSAL: Implement a community garden project in an urban neighborhood
GOAL: Improve food security and community cohesion
STAKEHOLDERS: Local residents, city government, environmental groups
"""

# Process (this will take 3-5 minutes)
results = orchestrator.process(scenario, case_name="community_garden_test")

# View summary
print(orchestrator.get_summary(results))
```

If this runs without errors, your installation is successful!

## Configuration

### Environment Variables

All configuration is done through environment variables in `.env`:

```bash
# Environment
TIKUN_ENV=development  # development, staging, production
LOG_LEVEL=INFO         # DEBUG, INFO, WARNING, ERROR, CRITICAL
OUTPUT_DIR=./results   # Where to save results

# Model Configuration (defaults shown)
KETER_MODEL=gemini-2.0-flash-exp
CHOCHMAH_MODEL=claude-3-5-sonnet-20241022
BINAH_WEST_MODEL=gemini-2.0-flash-exp
BINAH_EAST_MODEL=deepseek-chat
TIFERET_MODEL=claude-3-5-sonnet-20241022
YESOD_MODEL=claude-3-5-sonnet-20241022
MALCHUT_MODEL=claude-3-5-sonnet-20241022

# Performance
API_TIMEOUT=120
MAX_RETRIES=3
RATE_LIMIT_RPM=60

# BinahSigma
BINAH_SIGMA_THRESHOLD=0.15
BINAH_HIGH_DIVERGENCE_THRESHOLD=40
```

### Model Selection

You can customize which AI model is used for each Sefirah:

- **Gemini models**: `gemini-2.0-flash-exp`, `gemini-1.5-pro`, etc.
- **Claude models**: `claude-3-5-sonnet-20241022`, `claude-3-opus-20240229`, etc.
- **DeepSeek models**: `deepseek-chat`, `deepseek-coder`

## Running the RBU ONU Test Case

A comprehensive test case is included:

```bash
python test_rbu_onu_COMPATIBLE.py
```

This test analyzes a Universal Basic Income proposal funded by 1% military spending reduction. It's designed to trigger BinahSigma mode and takes approximately 3-5 minutes.

Expected output:
- JSON and TXT files in `results/` directory
- Console output showing each Sefirah's analysis
- BinahSigma analysis comparing Western vs Eastern perspectives

## Troubleshooting

### Common Issues

#### 1. API Key Errors

```
Error: GEMINI_API_KEY not found
```

**Solution**: Ensure `.env` file exists with valid API keys.

#### 2. Import Errors

```
ModuleNotFoundError: No module named 'tikun'
```

**Solution**: Install the package or add project root to PYTHONPATH:

```bash
# Option 1: Install package
pip install -e .

# Option 2: Add to PYTHONPATH (temporary)
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"  # macOS/Linux
set PYTHONPATH=%PYTHONPATH%;%cd%\src          # Windows
```

#### 3. Rate Limiting

```
Error: Rate limit exceeded
```

**Solution**: Adjust `RATE_LIMIT_RPM` in `.env` or add delays between runs.

#### 4. Timeout Errors

```
Error: Request timeout
```

**Solution**: Increase `API_TIMEOUT` in `.env` (default: 120 seconds).

### Getting Help

- **Documentation**: See `docs/` directory
- **Issues**: https://github.com/yourusername/tikun-olam/issues
- **Philosophy**: Read `PHILOSOPHY.md` for conceptual background
- **Architecture**: See `docs/ARCHITECTURE.md` (to be created)

## Development Setup

For contributors:

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Code formatting
black src/ tests/
isort src/ tests/

# Type checking
mypy src/

# Linting
flake8 src/ tests/
```

## Next Steps

1. Read the [Architecture Documentation](ARCHITECTURE.md) (to be created)
2. Explore the [BinahSigma Technical Spec](BINAH_SIGMA.md) (to be created)
3. Check the [API Reference](API.md) (to be created)
4. Review the [Philosophical Foundations](../PHILOSOPHY.md)

---

**Ready to repair the world (תיקון עולם)**
