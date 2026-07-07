# OOTD Creator

An AI-powered outfit generator built with Streamlit and Claude. Upload a clothing item, describe your vibe, and get a complete outfit suggestion in seconds.

## How it works

1. Upload a photo of the piece you want to build around
2. Describe the vibe you're going for (e.g. quiet luxury, y2k, office minimal)
3. Hit Generate OOTD — Claude analyzes the item and returns a full outfit: shoes, bottom, top, bag, accessories, and a styling tip

## Tech Stack

- Python 3.14
- Streamlit
- Anthropic Claude API (claude-sonnet-4-6) with vision
- Pillow

## Run locally

```bash
pip install -r requirements.txt
ANTHROPIC_API_KEY="your-key" streamlit run app.py
```

## Design

Minimal editorial aesthetic — Pinyon Script for the title, Helvetica Neue Light throughout, off-white background.