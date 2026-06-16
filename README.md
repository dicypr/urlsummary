# WebDigest — AI URL Summarizer

Give it a URL, get a snarky LLaMA-powered summary. Built from the Day 1 LLM Engineering notebook.

## Stack

- **Backend**: Python serverless function (Vercel)...
- **LLM**: LLaMA 3.3 70B via Groq API
- **Frontend**: Vanilla HTML/CSS/JS (no framework needed)

## Local Development

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create your .env file
echo "GROQ_API_KEY=gsk_your_key_here" > .env

# 3. Run a local dev server (simple option)
python -m http.server 8000 --directory static
# Then open http://localhost:8000
# Note: for full API testing locally, use the Vercel CLI (see below)
```

### Full local test with Vercel CLI

```bash
npm i -g vercel
vercel dev
# Opens at http://localhost:3000 with the API working
```

## Deploy to Vercel

### Option A: Via GitHub (recommended)

1. Push this folder to a GitHub repo
2. Go to [vercel.com](https://vercel.com) → New Project → Import your repo
3. Add environment variable: `GROQ_API_KEY` = your Groq key
4. Click Deploy — done!

### Option B: Via Vercel CLI

```bash
npm i -g vercel
vercel        # follow prompts, set GROQ_API_KEY when asked
```

## Get a Groq API Key

Free at [console.groq.com](https://console.groq.com) — no credit card needed.

## Limitations

- JavaScript-heavy sites (React SPAs, etc.) won't render correctly
- Sites behind Cloudflare or auth walls will return errors
- Page content is capped at 8,000 characters before sending to the LLM

## Project Structure

```
url-summarizer/
├── api/
│   └── summarize.py     # Vercel serverless function
├── static/
│   └── index.html       # Frontend (single file)
├── requirements.txt
├── vercel.json
└── .gitignore
```
