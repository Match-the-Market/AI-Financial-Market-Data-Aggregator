# MarketPulse AI

Web app that aggregates real-time news about any political or financially influential person and uses Google Gemini AI to analyze how their actions impact a market sector. Enter a name, pick a sector, get instant investor sentiment, market outlook, affected stocks, and an AI news summary.

> Not financial advice. This tool surfaces real market dynamics so retail investors can see what institutional traders already know.

---

## Setup

**Requirements:** Python 3.10+, [NewsAPI key](https://newsapi.org/), [Gemini API key](https://aistudio.google.com/)

```bash
git clone https://github.com/Match-the-Market/AI-Financial-Market-Data-Aggregator.git
cd AI-Financial-Market-Data-Aggregator
pip install -r requirements.txt
```

Create a `.env` file:

```
GENAI_API_KEY=your_gemini_key
NEWS_API_KEY=your_newsapi_key
```

```bash
python app.py        # dev — http://localhost:5000
gunicorn app:app     # production
```

---

## Usage

1. Type any political or financial figure's name (e.g. *Donald Trump*, *Jerome Powell*, *Elon Musk*)
2. Select a market sector
3. Click **Analyze** — results appear in seconds

**What you get:** investor sentiment, short/long-term outlook, 4 affected stocks, AI summary.

---

## How It Works

User input → NewsAPI fetches 5 recent articles → Gemini AI analyzes and returns structured JSON → Frontend renders color-coded results.

The `/analyze` endpoint accepts `POST { person, sector }` and returns JSON with `sentiment`, `shortTermOutlook`, `longTermOutlook`, `stocksAffected`, and `newsSummary`.

---

## Deployment

Set `GENAI_API_KEY` and `NEWS_API_KEY` as environment variables on your host (Render, Railway, Fly.io) and use `gunicorn app:app` as the start command.

