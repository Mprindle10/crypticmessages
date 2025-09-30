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
