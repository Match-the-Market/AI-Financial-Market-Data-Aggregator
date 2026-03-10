from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from google import genai
from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()

genai.configure(api_key=os.getenv("GENAI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')

NEWS_API_BASE_URL = "https://newsapi.org/v2/everything"

VALID_SECTORS = {
    "technology", "finance", "healthcare", "energy",
    "consumer", "industrials", "real estate", "utilities", "materials"
}


def get_news_articles(query, lang='en', page_size=5):
    params = {
        "q": query,
        "language": lang,
        "pageSize": page_size,
        "apiKey": os.getenv("NEWS_API_KEY"),
        "sortBy": "relevancy"
    }
    try:
        response = requests.get(NEWS_API_BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        articles = response.json().get('articles', [])
        combined_news = "\n\n".join(
            f"Title: {a['title']}\nDescription: {a['description']}"
            for a in articles if a.get('title') and a.get('description')
        )
        return combined_news
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return ""


def get_gemini_analysis(news_articles, person, sector):
    prompt = f"""
        Analyze the following news articles about {person}'s recent actions and their impact on the
        {sector} sector. Based on this, provide:

        1. Investor Sentiment (Bullish, Bearish, or Neutral) and explain why
        2. Short-Term Market Outlook (Up, Down, or Consolidate) and explain why
        3. Long-Term Market Outlook (Up, Down, or Consolidate) and explain why
        4. 4 popular stocks in this sector most likely to be affected, with predicted short-term movement.
        5. A concise, paragraph-long summary suitable for a financial news report and retail investor.

        Format your response strictly as a JSON object with no surrounding text, backticks, or markdown:
        {{
          "sentiment": "...",
          "whySentiment": "...",
          "shortTermOutlook": "...",
          "whyShortTermOutlook": "...",
          "longTermOutlook": "...",
          "whyLongTermOutlook": "...",
          "stocksAffected": [
            {{"ticker": "...", "movement": "..."}},
            {{"ticker": "...", "movement": "..."}},
            {{"ticker": "...", "movement": "..."}},
            {{"ticker": "...", "movement": "..."}}
          ],
          "newsSummary": "..."
        }}

        ---
        News Articles:
        {news_articles}
    """
    try:
        response = model.generate_content(prompt)
        cleaned_text = response.text.strip()
        if cleaned_text.startswith('```json'):
            cleaned_text = cleaned_text[7:]
        if cleaned_text.startswith('```'):
            cleaned_text = cleaned_text[3:]
        if cleaned_text.endswith('```'):
            cleaned_text = cleaned_text[:-3]
        cleaned_text = cleaned_text.strip()

        if not cleaned_text.startswith('{'):
            print("Gemini response was not valid JSON, using fallback.")
            return create_fallback_response(sector)

        return json.loads(cleaned_text)

    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        return create_fallback_response(sector)
    except Exception as e:
        print(f"Error calling Gemini: {e}")
        return create_fallback_response(sector)


def create_fallback_response(sector):
    return {
        "sentiment": "Neutral",
        "whySentiment": "Mixed market signals from recent news coverage.",
        "shortTermOutlook": "Consolidate",
        "whyShortTermOutlook": "Market is digesting recent political developments.",
        "longTermOutlook": "Up",
        "whyLongTermOutlook": f"{sector.title()} sector fundamentals remain intact despite short-term volatility.",
        "stocksAffected": [
            {"ticker": "AAPL", "movement": "Up"},
            {"ticker": "MSFT", "movement": "Up"},
            {"ticker": "GOOGL", "movement": "Consolidate"},
            {"ticker": "TSLA", "movement": "Down"}
        ],
        "newsSummary": (
            f"Recent developments show mixed impact on the {sector} sector. "
            "Investors are advised to monitor ongoing policy changes that may affect regulation and trade. "
            "Key stocks to watch as they navigate the current political and economic landscape."
        )
    }


app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze_sector():
    try:
        data = request.get_json(silent=True) or {}
        person = (data.get('person') or '').strip()
        sector = (data.get('sector') or 'technology').strip().lower()

        if not person:
            return jsonify({"error": "Please provide a person name to analyze."}), 400

        if sector not in VALID_SECTORS:
            sector = "technology"

        news_query = f"{person} AND {sector}"
        news_articles_text = get_news_articles(news_query)

        if not news_articles_text:
            return jsonify({"error": "Could not retrieve news articles. Please try again later."}), 500

        analysis_data = get_gemini_analysis(news_articles_text, person, sector)

        return jsonify({
            "person": person,
            "sector": sector,
            "sentiment": analysis_data.get('sentiment'),
            "whySentiment": analysis_data.get('whySentiment'),
            "shortTermOutlook": analysis_data.get('shortTermOutlook'),
            "whyShortTermOutlook": analysis_data.get('whyShortTermOutlook'),
            "longTermOutlook": analysis_data.get('longTermOutlook'),
            "whyLongTermOutlook": analysis_data.get('whyLongTermOutlook'),
            "stocksAffected": analysis_data.get('stocksAffected'),
            "newsSummary": analysis_data.get('newsSummary')
        }), 200

    except Exception as e:
        print(f"Server error in /analyze: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    if not os.getenv("GENAI_API_KEY"):
        print("WARNING: GENAI_API_KEY not loaded!")
    if not os.getenv("NEWS_API_KEY"):
        print("WARNING: NEWS_API_KEY not loaded!")
    app.run(debug=os.getenv("FLASK_DEBUG", "false").lower() == "true", port=5000)
