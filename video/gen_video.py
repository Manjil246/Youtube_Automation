# filepath: c:\Myself\News\code\video\gen_video.py
import os
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
from glob import glob

def create_video_from_images_and_audio(images_folder, audio_path, output_path):
    # Get all image file paths sorted
    image_files = sorted(
        glob(os.path.join(images_folder, "*")),
        key=lambda x: x.lower()
    )
    if not image_files:
        raise ValueError("No images found in the specified folder.")

    # Load audio and get its duration
    audio_clip = AudioFileClip(audio_path)
    audio_duration = audio_clip.duration
    n_images = len(image_files)
    duration_per_image = audio_duration / n_images

    # Create an ImageClip for each image with the calculated duration
    image_clips = [
        ImageClip(img).set_duration(duration_per_image).fadein(0.5).fadeout(0.5)
        for img in image_files
    ]

    # Concatenate image clips with crossfade transition
    video = concatenate_videoclips(
        image_clips, method="compose", padding=-0.5
    ).set_audio(audio_clip)

    # Set the video duration to match the audio exactly
    video = video.set_duration(audio_duration)

    # Write the result to a file
    video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")

if __name__ == "__main__":
    images_folder = os.path.join("images")
    audio_path = os.path.join("tts", "output.mp3")
    output_path = os.path.join("video", "output_video.mp4")
    os.makedirs("video", exist_ok=True)
    create_video_from_images_and_audio(images_folder, audio_path, output_path)
    print(f"Video created at {output_path}")
    images_folder = os.path.join("images")
    audio_path = os.path.join("tts", "output.mp3")
    output_path = os.path.join("video", "output_video.mp4")
    os.makedirs("video", exist_ok=True)

