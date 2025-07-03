import os
from openai import OpenAI
import json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_news_assets(details):
    prompt = f"""
You are a content assistant. Given the news details below, generate the following in JSON format:

1. voiceover_text: A concise but engaging voiceover script summarizing the news for a YouTube Shorts video.While keeping it under 120 words, ensure it captures the essence of the news and is suitable for a quick video format.Also when spoken, it should sound natural and engaging. And it should be within 30 seconds long when read aloud.
2. ai_image_prompt: A detailed text prompt suitable for generating an AI image representing the news. It should be descriptive enough for an AI image generator to create a relevant image. Include key elements from the news content, such as locations, people, and actions.
3. youtube_shorts_title: A catchy and SEO-friendly YouTube Shorts title (under 60 characters). It should be attention-grabbing and relevant to the news content, ideally including keywords that would help in search visibility.
4. youtube_tags: A list of relevant hashtags for the YouTube Shorts video. These should be popular and relevant to the news content, helping to increase visibility on YouTube. Include hashtags like #AI, #News, #Shorts, #YouTubeShorts.
4. youtube_description_disclaimer: A short disclaimer for the YouTube description about the content authenticity and AI use. It should be clear and concise. Then, a descriptive one line summary about the content.Also mention the news source and the authors name if mentioned. Also mention the news date and time if available. 

News Details(dumped as JSON):
Details : "{details}"

Output JSON format:
{{
  "voiceover_text": "...",
  "ai_image_prompt": "...",
  "youtube_shorts_title": "...",
  "youtube_tags": [...],
  "youtube_description_disclaimer": "..."
}}

Make sure the JSON is valid.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=500,
    )

    # Extract the JSON from the response
    text = response.choices[0].message.content
    
    # Sometimes the model adds ```json ... ``` markdown - clean it
    if text.startswith("```json"):
        text = text[len("```json"):].strip()
        if text.endswith("```"):
            text = text[:-3].strip()
    
    # Parse JSON safely
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        # fallback: try to extract json from text or return raw
        data = {"error": "Failed to parse JSON", "raw_response": text}
    
    return data

# Example usage:
if __name__ == "__main__":
    sample_news_content = {
        "source": {"id": "fox-news", "name": "Fox News"},
        "author": None,
        "title": "Feds bust Iranians in alleged human trafficking hub with terror links | Fox News Video",
        "description": "Assistant DHS Secretary Tricia McLaughlin joins 'America's Newsroom' to discuss federal agents arresting a group of Iranians in an alleged human trafficking hub near Los Angeles and a new app that alerts users about nearby ICE agents.",
        "url": "https://www.foxnews.com/video/6375054107112",
        "urlToImage": "https://a57.foxnews.com/cf-images.us-east-1.prod.boltdns.net/v1/static/694940094001/88dfc546-5665-48f6-826b-c7a3db197951/d353d47a-c52c-4962-afd4-19e926686646/1280x720/match/1024/512/image.jpg?ve=1&tl=1",
        "publishedAt": "2025-06-30T17:37:28.2045751Z",
        "content": "©2025 FOX News Network, LLC. All rights reserved. This material may not be published, broadcast, rewritten, or redistributed. All market data delayed 20 minutes."
    }

    assets = generate_news_assets(sample_news_content)
    with open("script/script_output.json", "w", encoding="utf-8") as f:
            json.dump(assets, f, ensure_ascii=False, indent=2)
    print(json.dumps(assets, indent=2, ensure_ascii=False))
