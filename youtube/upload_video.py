import os 
import google_auth_httplib2
import googleapiclient.discovery
import googleapiclient.errors
import googleapiclient.http
import google_auth_oauthlib
import json



SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def authenticate_youtube():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    client_secret  = "client_secret.json"

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secret,SCOPES
    )

    credentials = flow.run_local_server(port=0)

    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

    return youtube

def upload_video(youtube):
    # Load title and description from script_output.json
    with open("script/script_output.json", "r", encoding="utf-8") as f:
        meta = json.load(f)
    title = meta.get("youtube_shorts_title", "AI News Update").strip()
    description = meta.get("youtube_description_disclaimer", "This video is generated using AI and may not represent real events.").strip()
    tags = meta.get("youtube_tags", ["#AI", "#News", "#Shorts", "#YouTubeShorts"])

    request_body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": "22"  # Category ID for "People & Blogs"
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False
        }
    }

    media_file = "video\output_video.mp4"

    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=googleapiclient.http.MediaFileUpload(media_file,chunksize=-1, resumable=True)
    )

    response = None

    while response is None:
        try:
            status, response = request.next_chunk()
            if status:
                print(f"Uploading... {int(status.progress() * 100)}%")
        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}")
            return None

    print(f"Video uploaded successfully: {response['id']}")
    return response['id']


if __name__ == "__main__":
    youtube = authenticate_youtube()
    video_id = upload_video(youtube)
    if video_id:
        print(f"Video ID: {video_id}")
    else:
        print("Video upload failed.")