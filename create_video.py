#!/usr/bin/env python3
"""
YouTube Short Video Generator
Creates MP4 video from HTML/CSS animation using Selenium and Pillow
"""

import os
import time
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from PIL import Image
import tempfile
import shutil

def setup_chrome_driver():
    """Setup Chrome driver for headless operation"""
    print("🔧 Setting up Chrome driver...")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1080,1920")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--allow-running-insecure-content")
    
    try:
        # Try to use system Chrome/Chromium
        driver = webdriver.Chrome(options=chrome_options)
        print("✅ Chrome driver initialized")
        return driver
    except Exception as e:
        print(f"❌ Chrome driver error: {e}")
        print("📦 Installing Chrome...")
        install_chrome()
        return webdriver.Chrome(options=chrome_options)

def install_chrome():
    """Install Chrome if not available"""
    try:
        subprocess.run([
            "wget", "-q", "-O", "-", 
            "https://dl.google.com/linux/linux_signing_key.pub"
        ], check=True, capture_output=True)
        
        subprocess.run([
            "sudo", "apt", "update"
        ], check=True)
        
        subprocess.run([
            "sudo", "apt", "install", "-y", "google-chrome-stable"
        ], check=True)
        
        print("✅ Chrome installed successfully")
    except subprocess.CalledProcessError:
        print("⚠️ Installing Chromium as fallback...")
        subprocess.run([
            "sudo", "apt", "install", "-y", "chromium-browser"
        ], check=True)

def capture_frames(html_file, output_dir, duration=30, fps=30):
    """Capture frames from HTML animation"""
    print(f"📹 Capturing {duration}s video at {fps} fps...")
    
    driver = setup_chrome_driver()
    total_frames = duration * fps
    
    try:
        # Load HTML file
        html_path = f"file://{os.path.abspath(html_file)}"
        driver.get(html_path)
        
        # Wait for fonts to load
        time.sleep(2)
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Capture frames
        for frame in range(total_frames):
            # Take screenshot
            screenshot_path = os.path.join(output_dir, f"frame_{frame:04d}.png")
            driver.save_screenshot(screenshot_path)
            
            # Progress indicator
            if frame % 30 == 0:
                progress = (frame / total_frames) * 100
                print(f"📸 Progress: {progress:.1f}% ({frame}/{total_frames} frames)")
            
            # Wait for next frame
            time.sleep(1.0 / fps)
        
        print("✅ All frames captured successfully")
        
    finally:
        driver.quit()

def create_video_from_frames(frames_dir, output_file):
    """Convert frames to MP4 using FFmpeg"""
    print("🎬 Converting frames to MP4...")
    
    # Check if ffmpeg is installed
    try:
        subprocess.run(["ffmpeg", "-version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("📦 Installing FFmpeg...")
        subprocess.run(["sudo", "apt", "update"], check=True)
        subprocess.run(["sudo", "apt", "install", "-y", "ffmpeg"], check=True)
    
    # Create video from frames
    ffmpeg_cmd = [
        "ffmpeg", "-y",  # Overwrite output file
        "-framerate", "30",
        "-i", os.path.join(frames_dir, "frame_%04d.png"),
        "-c:v", "libx264",
        "-preset", "slow",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-r", "30",
        "-s", "1080x1920",
        "-movflags", "+faststart",
        output_file
    ]
    
    try:
        result = subprocess.run(ffmpeg_cmd, check=True, capture_output=True, text=True)
        print("✅ Video created successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ FFmpeg error: {e}")
        print(f"FFmpeg output: {e.stderr}")
        return False

def optimize_for_youtube(input_file, output_file):
    """Optimize video for YouTube Shorts"""
    print("🎯 Optimizing for YouTube Shorts...")
    
    optimize_cmd = [
        "ffmpeg", "-y",
        "-i", input_file,
        "-c:v", "libx264",
        "-preset", "slow",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-profile:v", "high",
        "-level", "4.0",
        "-r", "30",
        "-s", "1080x1920",
        "-movflags", "+faststart",
        "-maxrate", "8M",
        "-bufsize", "12M",
        output_file
    ]
    
    try:
        subprocess.run(optimize_cmd, check=True, capture_output=True)
        print("✅ YouTube optimization complete")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Optimization error: {e}")
        return False

def get_video_info(video_file):
    """Get video information using ffprobe"""
    try:
        cmd = [
            "ffprobe", "-v", "quiet",
            "-print_format", "json",
            "-show_format", "-show_streams",
            video_file
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("📊 Video Information:")
        print(f"📁 File: {video_file}")
        
        # Get file size
        size_bytes = os.path.getsize(video_file)
        size_mb = size_bytes / (1024 * 1024)
        print(f"💾 Size: {size_mb:.1f} MB")
        
        # Basic info
        print("📐 Resolution: 1080x1920 (9:16)")
        print("⏱️  Duration: 30 seconds")
        print("🎬 Frame Rate: 30 fps")
        
    except subprocess.CalledProcessError:
        print("⚠️ Could not get video info")

def main():
    """Main execution function"""
    print("🚀 The Riddle Room - YouTube Short Generator")
    print("=" * 50)
    
    # File paths
    html_file = "youtube_short_video.html"
    frames_dir = "youtube_video_output/frames"
    raw_video = "youtube_video_output/riddle_room_raw.mp4"
    final_video = "youtube_video_output/riddle_room_youtube_short.mp4"
    
    # Check if HTML file exists
    if not os.path.exists(html_file):
        print(f"❌ HTML file not found: {html_file}")
        return
    
    try:
        # Create output directory
        os.makedirs("youtube_video_output", exist_ok=True)
        
        # Step 1: Capture frames
        capture_frames(html_file, frames_dir, duration=30, fps=30)
        
        # Step 2: Create video from frames
        if create_video_from_frames(frames_dir, raw_video):
            
            # Step 3: Optimize for YouTube
            if optimize_for_youtube(raw_video, final_video):
                
                # Step 4: Get video info
                get_video_info(final_video)
                
                # Clean up frames
                shutil.rmtree(frames_dir, ignore_errors=True)
                os.remove(raw_video)
                
                print("\n🎉 SUCCESS! YouTube Short created!")
                print(f"📂 Output: {final_video}")
                print("\n📝 Upload Instructions:")
                print("1. Title: 'Can You Solve This Ancient Code? 🧠'")
                print("2. Description: Add your beta signup link")
                print("3. Hashtags: #puzzle #riddle #code #brain #genius")
                print("4. Category: Education")
                print("5. Upload as YouTube Short (vertical video)")
                
            else:
                print("❌ Video optimization failed")
        else:
            print("❌ Video creation failed")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("🛠️ Try running the bash script alternative: ./generate_youtube_video.sh")

if __name__ == "__main__":
    main()
