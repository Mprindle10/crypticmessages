#!/bin/bash

# YouTube Short Video Generator Script
# Creates MP4 from HTML animation

echo "🎬 Starting YouTube Short video generation..."

# Check if required tools are installed
check_dependencies() {
    echo "📋 Checking dependencies..."
    
    if ! command -v google-chrome &> /dev/null && ! command -v chromium-browser &> /dev/null; then
        echo "❌ Chrome/Chromium not found. Installing..."
        sudo apt update
        sudo apt install -y chromium-browser
    fi
    
    if ! command -v ffmpeg &> /dev/null; then
        echo "❌ FFmpeg not found. Installing..."
        sudo apt update
        sudo apt install -y ffmpeg
    fi
    
    echo "✅ Dependencies checked"
}

# Create video from HTML
generate_video() {
    echo "🎥 Generating video from HTML animation..."
    
    # Create output directory
    mkdir -p youtube_video_output
    
    # Set Chrome/Chromium path
    CHROME_PATH=""
    if command -v google-chrome &> /dev/null; then
        CHROME_PATH="google-chrome"
    elif command -v chromium-browser &> /dev/null; then
        CHROME_PATH="chromium-browser"
    fi
    
    # Generate video using headless browser and ffmpeg
    echo "📹 Recording HTML animation..."
    
    # Create a simple screen recording script
    cat > record_animation.js << 'EOF'
const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
    const browser = await puppeteer.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    const page = await browser.newPage();
    await page.setViewport({ width: 1080, height: 1920 });
    
    // Load the HTML file
    const htmlPath = 'file://' + process.cwd() + '/youtube_short_video.html';
    await page.goto(htmlPath, { waitUntil: 'networkidle0' });
    
    // Record for 30 seconds (30 frames per second = 900 frames)
    const frames = [];
    const fps = 30;
    const duration = 30; // seconds
    const totalFrames = fps * duration;
    
    console.log(`Recording ${totalFrames} frames at ${fps} fps...`);
    
    for (let i = 0; i < totalFrames; i++) {
        const frame = await page.screenshot({
            type: 'png',
            fullPage: false
        });
        
        fs.writeFileSync(`youtube_video_output/frame_${String(i).padStart(4, '0')}.png`, frame);
        
        if (i % 30 === 0) {
            console.log(`Progress: ${Math.round((i / totalFrames) * 100)}%`);
        }
        
        // Wait for next frame (1/30 second)
        await page.waitForTimeout(1000 / fps);
    }
    
    console.log('✅ All frames captured');
    await browser.close();
})();
EOF

    # Check if Node.js and Puppeteer are available
    if command -v node &> /dev/null && npm list puppeteer &> /dev/null; then
        echo "🎭 Using Puppeteer for high-quality recording..."
        node record_animation.js
    else
        echo "🎦 Using alternative ffmpeg recording method..."
        
        # Alternative: Use ffmpeg with xvfb for headless recording
        if command -v xvfb-run &> /dev/null; then
            echo "📺 Starting virtual display..."
            export DISPLAY=:99
            Xvfb :99 -screen 0 1080x1920x24 &
            XVFB_PID=$!
            
            # Open browser and record
            $CHROME_PATH --display=:99 --window-size=1080,1920 --start-fullscreen file://$(pwd)/youtube_short_video.html &
            BROWSER_PID=$!
            
            # Record screen
            ffmpeg -f x11grab -video_size 1080x1920 -framerate 30 -i :99.0 -t 30 -pix_fmt yuv420p youtube_video_output/riddle_room_short.mp4
            
            # Cleanup
            kill $BROWSER_PID
            kill $XVFB_PID
        else
            echo "🌐 Using HTML to image conversion..."
            # Fallback: Create static frames and animate
            create_fallback_video
        fi
    fi
    
    # Convert frames to video if we have individual frames
    if [ -d "youtube_video_output" ] && [ "$(ls -A youtube_video_output/frame_*.png 2>/dev/null)" ]; then
        echo "🎬 Converting frames to MP4..."
        ffmpeg -framerate 30 -i youtube_video_output/frame_%04d.png -c:v libx264 -pix_fmt yuv420p -crf 18 youtube_video_output/riddle_room_short.mp4
        
        # Clean up frame files
        rm youtube_video_output/frame_*.png
    fi
}

# Fallback method using HTML to image conversion
create_fallback_video() {
    echo "🖼️ Creating fallback video using image conversion..."
    
    # Install wkhtmltopdf for HTML to image conversion
    if ! command -v wkhtmltoimage &> /dev/null; then
        echo "📦 Installing wkhtmltoimage..."
        sudo apt update
        sudo apt install -y wkhtmltopdf
    fi
    
    # Create modified HTML files for different time points
    python3 << 'EOF'
import re
import os

# Read the original HTML
with open('youtube_short_video.html', 'r') as f:
    html_content = f.read()

# Create frames at key time points
keyframes = [0, 3, 8, 15, 25, 28, 30]
frame_dir = 'youtube_video_output'
os.makedirs(frame_dir, exist_ok=True)

for i, time in enumerate(keyframes):
    # Modify animation delays to show state at specific time
    modified_html = html_content
    
    # Adjust animation delays to show final states
    if time >= 25:  # Victory section
        modified_html = modified_html.replace('animation: victoryEnter 2s ease-out 25s forwards;', 
                                            'animation: victoryEnter 0s ease-out 0s forwards;')
        modified_html = modified_html.replace('animation: ctaEnter 1.5s ease-out 28s forwards;', 
                                            'animation: ctaEnter 0s ease-out 0s forwards;')
        modified_html = modified_html.replace('animation: brandEnter 1s ease-out 29s forwards;', 
                                            'animation: brandEnter 0s ease-out 0s forwards;')
    elif time >= 15:  # Transformation section
        modified_html = modified_html.replace('animation: transformationEnter 1s ease-out 15s forwards;', 
                                            'animation: transformationEnter 0s ease-out 0s forwards;')
    elif time >= 8:  # Teaching section
        modified_html = modified_html.replace('animation: teachingEnter 1.5s ease-out 8s forwards;', 
                                            'animation: teachingEnter 0s ease-out 0s forwards;')
    
    # Write modified HTML
    frame_file = f'{frame_dir}/frame_{i:04d}.html'
    with open(frame_file, 'w') as f:
        f.write(modified_html)

print(f"Created {len(keyframes)} keyframe HTML files")
EOF

    # Convert HTML files to images
    for html_file in youtube_video_output/frame_*.html; do
        frame_num=$(basename "$html_file" .html | sed 's/frame_//')
        echo "📸 Converting $html_file to image..."
        wkhtmltoimage --width 1080 --height 1920 --format png "$html_file" "youtube_video_output/image_${frame_num}.png"
    done
    
    # Create video from images with crossfade
    echo "🎞️ Creating video with smooth transitions..."
    ffmpeg -framerate 1 -i youtube_video_output/image_%04d.png -vf "minterpolate=fps=30:mi_mode=mci" -t 30 -pix_fmt yuv420p youtube_video_output/riddle_room_short.mp4
    
    # Clean up
    rm youtube_video_output/frame_*.html
    rm youtube_video_output/image_*.png
}

# Optimize video for YouTube
optimize_for_youtube() {
    echo "🎯 Optimizing video for YouTube Shorts..."
    
    if [ -f "youtube_video_output/riddle_room_short.mp4" ]; then
        # Create YouTube-optimized version
        ffmpeg -i youtube_video_output/riddle_room_short.mp4 \
            -c:v libx264 \
            -preset slow \
            -crf 18 \
            -pix_fmt yuv420p \
            -r 30 \
            -s 1080x1920 \
            -movflags +faststart \
            youtube_video_output/riddle_room_youtube_short.mp4
        
        echo "✅ YouTube-optimized video created: youtube_video_output/riddle_room_youtube_short.mp4"
        
        # Get file info
        echo "📊 Video Information:"
        ffprobe -v quiet -print_format json -show_format -show_streams youtube_video_output/riddle_room_youtube_short.mp4
        
        echo ""
        echo "🎉 Video generation complete!"
        echo "📁 Output file: youtube_video_output/riddle_room_youtube_short.mp4"
        echo "📐 Resolution: 1080x1920 (9:16 aspect ratio)"
        echo "⏱️  Duration: 30 seconds"
        echo "🎬 Ready for YouTube Shorts upload!"
    else
        echo "❌ Error: Video file not found"
        exit 1
    fi
}

# Main execution
main() {
    echo "🚀 The Riddle Room - YouTube Short Generator"
    echo "============================================"
    
    check_dependencies
    generate_video
    optimize_for_youtube
    
    echo ""
    echo "🎊 SUCCESS! Your YouTube Short is ready!"
    echo "📂 Location: $(pwd)/youtube_video_output/riddle_room_youtube_short.mp4"
    echo ""
    echo "📝 Next steps:"
    echo "1. Upload to YouTube as a Short"
    echo "2. Title: 'Can You Solve This Ancient Code? 🧠'"
    echo "3. Add description with link to your beta page"
    echo "4. Use hashtags: #puzzle #riddle #code #brain #genius"
}

# Run the script
main
