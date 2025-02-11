# TikTok Video Creator

## Description
This script automatically creates short TikTok videos using downloaded video files and audio tracks. The video is supplemented with text provided by the user.

## Features
- Download videos from a YouTube playlist or a single video
- Download audio from a YouTube playlist or a single video
- Use pre-prepared mp3 files as audio
- Automatic trimming and centering of video
- Text wrapping for readability
- Flexible parameter configuration via command line
- Interactive parameter input if not specified in the command line
- Custom output video resolution settings

## Installation
1. Install Python 3.7+
2. Install the required dependencies:
   ```bash
   pip install pytubefix moviepy
   ```

## Usage

### Downloading Videos and Audio
Download a video or playlist from YouTube:
```bash
python generate.py --download_visuals <URL>
```
Download audio or playlist from YouTube:
```bash
python generate.py --download_music <URL>
```

### Creating a Video
Create a video with user-defined text:
```bash
python generate.py --text "Track Name" --duration 10
```
Use an external mp3 file from the `music/` folder:
```bash
python generate.py --text "Track Name" --duration 10 --external_audio
```
Set custom output video dimensions:
```bash
python generate.py --text "Track Name" --duration 10 --width 1920 --height 1080
```

### Command Line Arguments
- `--download_visuals <URL>` — Download a video or playlist from YouTube
- `--download_music <URL>` — Download audio or playlist from YouTube
- `--text <TEXT>` — Text overlay for the video
- `--duration <SECONDS>` — Final video duration (default: 7 seconds)
- `--width <PIXELS>` — Output video width (default: 1080)
- `--height <PIXELS>` — Output video height (default: 1080)
- `--external_audio` — Use an external mp3 file instead of extracting audio from the video
- `--full_audio_length` — Adjust video duration to match the full length of the audio track

### Interactive Input
If parameters are not provided in the command line, the script will prompt the user to enter them interactively.

