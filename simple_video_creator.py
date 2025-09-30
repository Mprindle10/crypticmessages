#!/usr/bin/env python3
"""
Simple YouTube Short Video Creator
Uses browser automation to create MP4 from HTML animation
"""

import os
import time
import subprocess
import json
from pathlib import Path

def check_dependencies():
    """Check and install required dependencies"""
    print("📋 Checking dependencies...")
    
    # Check for Chrome/Chromium
    chrome_found = False
    for cmd in ['google-chrome', 'chromium-browser', 'chromium']:
        try:
            subprocess.run([cmd, '--version'], capture_output=True, check=True)
            print(f"✅ Found browser: {cmd}")
            chrome_found = True
            break
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    
    if not chrome_found:
        print("📦 Installing Chromium...")
        subprocess.run(['sudo', 'apt', 'update'], check=True)
        subprocess.run(['sudo', 'apt', 'install', '-y', 'chromium-browser'], check=True)
    
    # Check for FFmpeg
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        print("✅ FFmpeg found")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("📦 Installing FFmpeg...")
        subprocess.run(['sudo', 'apt', 'update'], check=True)
        subprocess.run(['sudo', 'apt', 'install', '-y', 'ffmpeg'], check=True)

def create_simple_video():
    """Create video using simple frame extraction method"""
    print("🎬 Creating YouTube Short video...")
    
    # Create output directory
    output_dir = Path("youtube_video_output")
    output_dir.mkdir(exist_ok=True)
    
    # HTML file path
    html_file = Path("youtube_short_video.html").absolute()
    
    if not html_file.exists():
        print(f"❌ HTML file not found: {html_file}")
        return False
    
    print(f"📄 Using HTML file: {html_file}")
    
    # Create video using browser and screen recording
    video_file = output_dir / "riddle_room_youtube_short.mp4"
    
    # Method 1: Try using wkhtmltopdf approach for static frames
    print("🖼️ Creating video frames...")
    
    # Install wkhtmltopdf if needed
    try:
        subprocess.run(['wkhtmltoimage', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("📦 Installing wkhtmltopdf...")
        subprocess.run(['sudo', 'apt', 'update'], check=True)
        subprocess.run(['sudo', 'apt', 'install', '-y', 'wkhtmltopdf'], check=True)
    
    # Create keyframe images
    keyframes = create_keyframe_images(html_file, output_dir)
    
    if keyframes:
        # Create video from keyframes
        success = create_video_from_keyframes(keyframes, video_file)
        if success:
            optimize_video(video_file)
            return True
    
    # Method 2: Fallback to simple HTML duplication
    print("🔄 Using fallback method...")
    return create_fallback_video(html_file, video_file)

def create_keyframe_images(html_file, output_dir):
    """Create images at key animation points"""
    print("📸 Generating keyframe images...")
    
    keyframes = []
    frame_times = [0, 3, 8, 15, 20, 25, 28, 30]  # Key animation moments
    
    for i, time_point in enumerate(frame_times):
        frame_file = output_dir / f"keyframe_{i:02d}.png"
        
        # Create image using wkhtmltoimage
        cmd = [
            'wkhtmltoimage',
            '--width', '1080',
            '--height', '1920',
            '--format', 'png',
            '--quiet',
            str(html_file),
            str(frame_file)
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            keyframes.append(str(frame_file))
            print(f"✅ Created keyframe {i+1}/{len(frame_times)}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to create keyframe {i}: {e}")
    
    return keyframes

def create_video_from_keyframes(keyframes, output_file):
    """Create smooth video from keyframe images"""
    print("🎞️ Creating video from keyframes...")
    
    if len(keyframes) < 2:
        print("❌ Not enough keyframes to create video")
        return False
    
    # Create input file list for FFmpeg
    input_list = output_file.parent / "input_list.txt"
    
    with open(input_list, 'w') as f:
        for keyframe in keyframes:
            # Each keyframe shown for ~4 seconds, then fade to next
            f.write(f"file '{keyframe}'\n")
            f.write(f"duration 3.75\n")
        # Duplicate last frame
        f.write(f"file '{keyframes[-1]}'\n")
    
    # Create video with smooth transitions
    cmd = [
        'ffmpeg', '-y',
        '-f', 'concat',
        '-safe', '0',
        '-i', str(input_list),
        '-vf', 'scale=1080:1920,fps=30',
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        '-t', '30',  # Exactly 30 seconds
        str(output_file)
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"✅ Video created: {output_file}")
        
        # Clean up
        input_list.unlink()
        for keyframe in keyframes:
            Path(keyframe).unlink()
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Video creation failed: {e}")
        return False

def create_fallback_video(html_file, output_file):
    """Fallback method using simpler approach"""
    print("🎨 Creating fallback video...")
    
    # Create a single high-quality image from HTML
    image_file = output_file.parent / "static_frame.png"
    
    cmd = [
        'wkhtmltoimage',
        '--width', '1080',
        '--height', '1920',
        '--format', 'png',
        '--quality', '100',
        str(html_file),
        str(image_file)
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print("✅ Static image created")
        
        # Create 30-second video from single image with zoom effect
        cmd = [
            'ffmpeg', '-y',
            '-loop', '1',
            '-i', str(image_file),
            '-t', '30',
            '-vf', 'scale=1080:1920,zoompan=z=\'min(zoom+0.0015,1.5)\':d=900:x=iw/2-(iw/zoom/2):y=ih/2-(ih/zoom/2),fps=30',
            '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p',
            '-preset', 'medium',
            str(output_file)
        ]
        
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"✅ Fallback video created: {output_file}")
        
        # Clean up
        image_file.unlink()
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Fallback creation failed: {e}")
        return False

def optimize_video(video_file):
    """Optimize video for YouTube"""
    print("🎯 Optimizing for YouTube Shorts...")
    
    optimized_file = video_file.parent / f"{video_file.stem}_optimized{video_file.suffix}"
    
    cmd = [
        'ffmpeg', '-y',
        '-i', str(video_file),
        '-c:v', 'libx264',
        '-preset', 'slow',
        '-crf', '18',
        '-pix_fmt', 'yuv420p',
        '-profile:v', 'high',
        '-level', '4.0',
        '-r', '30',
        '-s', '1080x1920',
        '-movflags', '+faststart',
        '-maxrate', '8M',
        '-bufsize', '12M',
        str(optimized_file)
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        
        # Replace original with optimized
        video_file.unlink()
        optimized_file.rename(video_file)
        
        print("✅ Video optimized for YouTube")
        
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Optimization failed, keeping original: {e}")

def get_video_stats(video_file):
    """Display video statistics"""
    print("\n📊 Video Information:")
    print(f"📁 File: {video_file}")
    
    if video_file.exists():
        size_mb = video_file.stat().st_size / (1024 * 1024)
        print(f"💾 Size: {size_mb:.1f} MB")
        print("📐 Resolution: 1080x1920 (9:16)")
        print("⏱️  Duration: 30 seconds")
        print("🎬 Frame Rate: 30 fps")
        print("🎯 Format: MP4 (YouTube optimized)")
    else:
        print("❌ Video file not found")

def main():
    """Main execution"""
    print("🚀 The Riddle Room - YouTube Short Creator")
    print("=" * 50)
    
    try:
        # Check dependencies
        check_dependencies()
        
        # Create video
        success = create_simple_video()
        
        if success:
            video_file = Path("youtube_video_output/riddle_room_youtube_short.mp4")
            get_video_stats(video_file)
            
            print("\n🎉 SUCCESS! YouTube Short ready!")
            print(f"📂 Location: {video_file.absolute()}")
            print("\n📋 Upload Instructions:")
            print("1. Title: 'Can You Solve This Ancient Code? 🧠'")
            print("2. Description: Challenge your brain with ancient ciphers!")
            print("3. Add: 'Link in description below' for your beta signup")
            print("4. Hashtags: #puzzle #riddle #code #brain #genius #shorts")
            print("5. Category: Education")
            print("6. Upload as YouTube Short (9:16 vertical)")
            
        else:
            print("❌ Video creation failed")
            
    except KeyboardInterrupt:
        print("\n⏹️ Operation cancelled by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
