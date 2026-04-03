#!/usr/bin/env python3
"""
Mi Abuelita Meri - SIMPLEST VIDEO CREATOR
ONE Image + ALL Audio = ONE Video
NO effects, NO transitions - just the image with audio
This will be FAST!
"""

import os
import glob
import subprocess
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# Get ffmpeg path from moviepy
from moviepy.config import FFMPEG_BINARY
FFMPEG = FFMPEG_BINARY
FFPROBE = FFMPEG.replace("ffmpeg", "ffprobe")

def create_simple_video():
    """Create a simple video with one image and all audio"""
    
    # Paths
    workspace = os.path.join("..", "workspace")
    images_dir = os.path.join(workspace, "output", "images")
    audio_dir = os.path.join(workspace, "output", "audio")
    videos_dir = os.path.join(workspace, "output", "videos")
    
    # Get first image and all audio files
    image_files = sorted(glob.glob(os.path.join(images_dir, "scene_*.png")))
    audio_files = sorted(glob.glob(os.path.join(audio_dir, "scene_*_audio.mp3")))
    
    print(f"Found {len(image_files)} images and {len(audio_files)} audio files")
    
    if not image_files or not audio_files:
        print("ERROR: No images or audio found!")
        return
    
    # Use first image
    image_path = image_files[0]
    print(f"Using image: {image_path}")
    
    # Create a file list for ffmpeg concatenation
    concat_file = os.path.join(videos_dir, "concat_list.txt")
    with open(concat_file, 'w') as f:
        for audio in audio_files:
            f.write(f"file '{os.path.abspath(audio)}'\n")
    
    # Concatenate all audio files
    combined_audio = os.path.join(videos_dir, "combined_audio.mp3")
    print("Concatenating audio files...")
    
    subprocess.run([
        FFMPEG, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_file,
        "-c", "copy",
        combined_audio
    ], capture_output=True)
    
    if not os.path.exists(combined_audio):
        print("ERROR: Failed to concatenate audio!")
        return
    
    # Get audio duration
    result = subprocess.run([
        FFPROBE, "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        combined_audio
    ], capture_output=True, text=True)
    
    duration = float(result.stdout.strip())
    print(f"Total audio duration: {duration/60:.1f} minutes")
    
    # Create video with ffmpeg (MUCH faster than moviepy!)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(videos_dir, f"mega_episode_{timestamp}.mp4")
    
    print("Creating video with ffmpeg (fast!)...")
    
    subprocess.run([
        FFMPEG, "-y",
        "-loop", "1",
        "-i", image_path,
        "-i", combined_audio,
        "-c:v", "libx264",
        "-tune", "stillimage",
        "-c:a", "aac",
        "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-shortest",
        output_file
    ], capture_output=True)
    
    if os.path.exists(output_file):
        size_mb = os.path.getsize(output_file) / (1024 * 1024)
        print(f"\n✅ SUCCESS!")
        print(f"Video: {output_file}")
        print(f"Size: {size_mb:.1f} MB")
        print(f"Duration: {duration/60:.1f} minutes")
    else:
        print("ERROR: Failed to create video!")

if __name__ == "__main__":
    print("=" * 60)
    print("  SIMPLE VIDEO CREATOR")
    print("  ONE Image + ALL Audio = ONE Video")
    print("  Fast rendering with ffmpeg!")
    print("=" * 60)
    print()
    
    create_simple_video()
