import os
import sys
import argparse
from pytubefix import Playlist, YouTube
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip
from random import choice
from moviepy.config import change_settings
from datetime import datetime

def is_playlist(url):
    """Determines whether the URL is a playlist or a single video."""
    return 'list=' in url

def download_videos(url):
    """Downloads videos (from a playlist or a single video)."""
    print("Downloading videos...")
    save_path = os.path.join(os.getcwd(), 'visual')
    os.makedirs(save_path, exist_ok=True)
    
    if is_playlist(url):
        urls = Playlist(url)
    else:
        urls = [url]
    
    for video_url in urls:
        try:
            yt = YouTube(video_url)
            print(f"Downloading: {yt.title} ({yt.length} seconds)")
            yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(
                output_path=save_path, filename=f"{yt.length}_{yt.title}.mp4")
            print("Done!")
        except Exception as e:
            print(f"Error downloading video: {e}")

def download_music(url):
    """Downloads audio (from a playlist or a single video)."""
    print("Downloading music...")
    save_path = os.path.join(os.getcwd(), 'music')
    os.makedirs(save_path, exist_ok=True)
    
    if is_playlist(url):
        urls = Playlist(url)
    else:
        urls = [url]
    
    for video_url in urls:
        try:
            yt = YouTube(video_url)
            print(f"Downloading: {yt.title}")
            yt.streams.filter(only_audio=True).order_by('abr').desc().first().download(output_path=save_path)
            print("Done!")
        except Exception as e:
            print(f"Error downloading audio: {e}")

def calculate_max_chars_per_line(width):
    """Calculates the maximum number of characters per line based on video width."""
    # Example: for width 1080, max characters ~1080//40 = 27; adjust as needed.
    return max(10, width // 50)

def split_text(text, width):
    """Splits text into multiple lines based on video width."""
    max_chars_per_line = calculate_max_chars_per_line(width)
    words = text.split()
    lines = []
    current_line = ""
    
    for word in words:
        if len(current_line) + len(word) + (1 if current_line else 0) <= max_chars_per_line:
            current_line += (" " + word if current_line else word)
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    
    return "\n".join(lines)

def create_video_with_music(text, video_duration, use_external_audio, full_audio_length, width, height):
    """Creates a video with overlaid text and background music."""
    visual_folder = os.path.join(os.getcwd(), 'visual')
    music_folder = os.path.join(os.getcwd(), 'music')
    final_folder = os.path.join(os.getcwd(), 'final')
    
    os.makedirs(music_folder, exist_ok=True)
    os.makedirs(final_folder, exist_ok=True)
    
    try:
        video_file = choice(os.listdir(visual_folder))
        video_path = os.path.join(visual_folder, video_file)
        clip = VideoFileClip(video_path, audio=False)
        
        if use_external_audio:
            music_files = [f for f in os.listdir(music_folder) if f.endswith('.mp3')]
        else:
            music_files = os.listdir(music_folder)
        
        if not music_files:
            raise ValueError("No available audio files!")
        music_file = choice(music_files)
        music_path = os.path.join(music_folder, music_file)
        music = AudioFileClip(music_path)
        
        if full_audio_length:
            video_duration = music.duration
        
        clip = clip.subclip(0, video_duration)
        clip = clip.resize((width, height))
        
        formatted_text = split_text(text, width)
        text_clip = TextClip(formatted_text, color="white", fontsize=80, font="Arial-Bold", stroke_color="black", stroke_width=3)
        text_clip = text_clip.set_position("center").set_duration(video_duration)
        final_clip = CompositeVideoClip([clip, text_clip]).set_audio(music)
        
        output_path = os.path.join(final_folder, f"final_video_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.mp4")
        final_clip.write_videofile(output_path, codec="libx264", fps=24)
        print(f"Video saved: {output_path}")
    except Exception as e:
        print(f"Error creating video: {e}")

def parse_arguments():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-dv", "--download_visuals", type=str, help="URL of the video or playlist to download visuals")
    parser.add_argument("-dm", "--download_music", type=str, help="URL of the video or playlist to download music")
    parser.add_argument("-t", "--text", type=str, help="Text to overlay on the video")
    parser.add_argument("-d", "--duration", type=int, default=7, help="Final video duration in seconds")
    parser.add_argument("-ea", "--external_audio", action="store_true", help="Use external mp3 files")
    parser.add_argument("-fal", "--full_audio_length", action="store_true", help="Use full audio length instead of fixed video duration")
    parser.add_argument("-w", "--width", type=int, default=1080, help="Output video width")
    parser.add_argument("-ht", "--height", type=int, default=1080, help="Output video height")
    return parser.parse_args()

def main():
    change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})
    args = parse_arguments()
    
    # Interactive input for downloading visuals
    if not args.download_visuals:
        dv_input = input("Enter URL for downloading visuals (leave empty if not needed): ").strip()
        if dv_input:
            args.download_visuals = dv_input
            download_videos(args.download_visuals)
    
    # Interactive input for downloading music
    if not args.download_music:
        dm_input = input("Enter URL for downloading music (leave empty if not needed): ").strip()
        if dm_input:
            args.download_music = dm_input
            download_music(args.download_music)
    
    # Interactive input for video parameters if not provided via command-line
    if len(sys.argv) == 1:  # No command-line arguments provided
        duration_input = input("Enter video duration in seconds (default 7): ").strip()
        duration = int(duration_input) if duration_input.isdigit() else 7
        
        width_input = input("Enter video width (default 1080): ").strip()
        width = int(width_input) if width_input.isdigit() else 1080
        
        height_input = input("Enter video height (default 1080): ").strip()
        height = int(height_input) if height_input.isdigit() else 1080
    else:
        duration = args.duration
        width = args.width
        height = args.height

    text = args.text if args.text else input("Enter text for the video: ")
    create_video_with_music(text, duration, args.external_audio, args.full_audio_length, width, height)

if __name__ == "__main__":
    main()
