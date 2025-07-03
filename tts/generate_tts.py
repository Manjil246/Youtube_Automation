import os
import openai

def generate_tts(text, voice):
    mp3_path = "tts/output.mp3"
    openai.api_key = os.getenv("OPENAI_API_KEY")
    # Optionally, fallback to hardcoded key for testing ONLY (not recommended)
    # openai.api_key = "sk-..."  # Uncomment and insert your key if needed

    # Call OpenAI TTS API
    response = openai.audio.speech.create(
        model="tts-1",
        voice=voice,
        input= text
    )

    # Save the mp3 file
    with open(mp3_path, "wb") as f:
        f.write(response.content)

    print(f"Generated file: {mp3_path}")
    return mp3_path


if __name__ == "__main__":
    text = "In a shocking development, federal agents have busted a group of Iranians in an alleged human trafficking hub near Los Angeles. Assistant DHS Secretary Tricia McLaughlin shared insights on America's Newsroom about this serious situation, which also links to potential terror activities. The authorities are not just stopping at arrests; a new app is set to alert users about nearby ICE agents, adding another layer to this ongoing saga. Stay tuned for more updates on this alarming case."
    voice = "nova"
    generate_tts(text, voice)