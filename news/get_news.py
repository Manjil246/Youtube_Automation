import os
import requests
import json
from datetime import datetime

NEWS_API_KEY = os.getenv("NEWS_API_KEY")  # Set your NewsAPI key as an environment variable

def get_top_headlines():
    url = "https://newsapi.org/v2/top-headlines"
    today = datetime.utcnow().strftime("%Y-%m-%d")
    params = {
        "sources": "bbc-news,cnn,fox-news,al-jazeera-english",
        "apiKey": NEWS_API_KEY,
        "pageSize": 100,
        "publishedAt": today
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return data.get("articles", [])

if __name__ == "__main__":
    try:
        articles = get_top_headlines()
        # Add publishedAt field to output
        output = articles
        os.makedirs("news", exist_ok=True)
        with open("news/news_output.json", "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        print(f"Wrote {len(output)} articles to news/news_output.json")
    except requests.RequestException as e:
        print(f"Error fetching news: {e}")
