# 📊 MarketPulse AI — Political & Financial Influence Tracker

MarketPulse AI is a web application that aggregates real-time news about any political or financially influential person and uses Google Gemini AI to analyze how their recent actions may impact a chosen market sector. It provides investor sentiment, short- and long-term market outlooks, affected stocks, and an AI-generated news summary — all in seconds.

> **Disclaimer:** This tool is for informational and educational purposes only. It does not constitute financial advice. The developers are not responsible for any investment decisions made based on this application.

---

## Table of Contents

- [Features](#features)
- [How It Works](#how-it-works)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
  - [Running the App](#running-the-app)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Supported Sectors](#supported-sectors)
- [Deployment](#deployment)
- [Contributing](#contributing)

---

## Features

- **Any person, any sector** — Search by any political figure (e.g. Donald Trump, Xi Jinping, Janet Yellen) or financial influencer (e.g. Warren Buffett, Elon Musk) across 9 market sectors.
- **Real-time news aggregation** — Pulls the latest relevant headlines via [NewsAPI](https://newsapi.org/).
- **AI-powered analysis** — Google Gemini AI reads the news and generates structured market analysis, including:
  - Investor sentiment (Bullish / Bearish / Neutral)
  - Short-term and long-term market outlook
  - 4 affected stock tickers with predicted movement direction
  - Plain-English news summary for retail investors
- **Polished, responsive UI** — Dark-themed interface with color-coded indicators and quick-select suggestion chips.

---

## How It Works

```
User enters a person + sector
         │
         ▼
Flask backend receives POST /analyze
         │
         ▼
NewsAPI fetches 5 recent articles matching "{person} AND {sector}"
         │
         ▼
Gemini AI reads the articles and returns structured JSON analysis
         │
         ▼
Frontend renders sentiment, outlooks, stocks, and summary
```

1. The user types a person's name (or clicks a suggestion chip) and selects a market sector.
2. The frontend sends a `POST /analyze` request with `{ person, sector }`.
3. The Flask backend queries **NewsAPI** for the 5 most relevant recent articles.
4. The combined article text is sent to **Google Gemini** with a structured prompt asking for JSON market analysis.
5. The JSON response is parsed, validated, and returned to the frontend.
6. The UI renders color-coded results — green for bullish/up, red for bearish/down, orange for neutral/consolidate.

---

## Tech Stack

| Layer     | Technology                          |
|-----------|-------------------------------------|
| Backend   | Python 3, Flask, flask-cors         |
| AI        | Google Gemini (`gemini-2.5-flash`)  |
| News Data | NewsAPI (`/v2/everything`)          |
| Frontend  | Vanilla HTML, CSS, JavaScript       |
| Config    | python-dotenv                       |
| Deploy    | Gunicorn (compatible with Render)   |

---

## Project Structure

```
AI-Financial-Market-Data-Aggregator/
├── app.py                  # Main Flask application
├── newsAPI.py              # Standalone NewsAPI helper module
├── requirements.txt        # Python dependencies
├── .env                    # API keys (not committed — see below)
├── templates/
│   └── index.html          # Main single-page UI
└── assets/
    └── placeImageshere.txt
```

---

## Getting Started

### Prerequisites

- Python 3.10 or higher
- A [NewsAPI](https://newsapi.org/) API key (free tier available)
- A [Google Gemini](https://aistudio.google.com/) API key (free tier available)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Match-the-Market/AI-Financial-Market-Data-Aggregator.git
cd AI-Financial-Market-Data-Aggregator

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root (never commit this file):

```env
GENAI_API_KEY=your_google_gemini_api_key_here
NEWS_API_KEY=your_newsapi_key_here
```

| Variable       | Where to get it                                       |
|----------------|-------------------------------------------------------|
| `GENAI_API_KEY`| [Google AI Studio](https://aistudio.google.com/)     |
| `NEWS_API_KEY` | [NewsAPI dashboard](https://newsapi.org/account)     |

### Running the App

```bash
python app.py
```

The app will start on `http://localhost:5000`. Open this URL in your browser.

For production use:

```bash
gunicorn app:app
```

---

## Usage

1. **Enter a name** — Type any political or financially influential person's name in the search box. Quick-select chips are provided for common names: Donald Trump, Jerome Powell, Elon Musk, Janet Yellen, Xi Jinping, and Warren Buffett.
2. **Select a sector** — Choose the market sector you want to analyze from the dropdown.
3. **Click "Analyze Market Impact"** — The app fetches recent news and returns an AI analysis within a few seconds.
4. **Read the results**:
   - **Investor Sentiment** — Overall mood of the market (Bullish / Bearish / Neutral) with reasoning.
   - **Short-Term Outlook** — Expected near-term price direction (Up / Down / Consolidate).
   - **Long-Term Outlook** — Expected longer-term price direction with reasoning.
   - **Stocks to Watch** — 4 tickers in the sector with predicted movement.
   - **AI News Summary** — A concise paragraph explaining the market dynamics.

### Example queries

| Person          | Sector      | What you might learn                                       |
|-----------------|-------------|-------------------------------------------------------------|
| Donald Trump    | Technology  | How trade tariffs or executive orders affect big tech       |
| Jerome Powell   | Finance     | Impact of Fed rate decision signals on banking stocks       |
| Elon Musk       | Consumer    | How Tesla news and social media influence consumer sentiment |
| Janet Yellen    | Energy      | Treasury policy effects on energy markets                   |
| Xi Jinping      | Materials   | How China policy shifts affect global commodities           |

---

## API Reference

### `POST /analyze`

Analyzes the market impact of a person's recent actions on a given sector.

**Request body (JSON):**

```json
{
  "person": "Donald Trump",
  "sector": "technology"
}
```

| Field    | Type   | Required | Description                          |
|----------|--------|----------|--------------------------------------|
| `person` | string | Yes      | Name of the political/financial figure |
| `sector` | string | No       | Market sector (defaults to `technology`) |

**Successful response (200):**

```json
{
  "person": "Donald Trump",
  "sector": "technology",
  "sentiment": "Bearish",
  "whySentiment": "...",
  "shortTermOutlook": "Down",
  "whyShortTermOutlook": "...",
  "longTermOutlook": "Up",
  "whyLongTermOutlook": "...",
  "stocksAffected": [
    { "ticker": "AAPL", "movement": "Down" },
    { "ticker": "MSFT", "movement": "Consolidate" },
    { "ticker": "NVDA", "movement": "Down" },
    { "ticker": "GOOGL", "movement": "Down" }
  ],
  "newsSummary": "..."
}
```

**Error response (400 / 500):**

```json
{ "error": "Please provide a person name to analyze." }
```

---

## Supported Sectors

| Sector       | Value to send   |
|--------------|-----------------|
| Technology   | `technology`    |
| Finance      | `finance`       |
| Healthcare   | `healthcare`    |
| Energy       | `energy`        |
| Consumer     | `consumer`      |
| Industrials  | `industrials`   |
| Real Estate  | `real estate`   |
| Utilities    | `utilities`     |
| Materials    | `materials`     |

---

## Deployment

The app is compatible with any platform that runs Python/Gunicorn. Example deployment on **Render**:

1. Set environment variables (`GENAI_API_KEY`, `NEWS_API_KEY`) in the Render dashboard.
2. Set the start command to `gunicorn app:app`.
3. Render will automatically detect `requirements.txt` and install dependencies.

For **Railway**, **Fly.io**, or similar platforms the setup is analogous — provide environment variables and use `gunicorn app:app` as the start command.

---

## Contributing

Pull requests are welcome. For significant changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m 'Add my feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request

