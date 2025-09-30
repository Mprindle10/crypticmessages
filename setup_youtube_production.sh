#!/bin/bash

# YouTube Short #1 Production Script
# Cipher Academy - Caesar Cipher Challenge

echo "🎬 Starting YouTube Short #1 Production Setup..."

# Create production directory
mkdir -p youtube_production/short_1
cd youtube_production/short_1

echo "📁 Created production directory: youtube_production/short_1"

# Create shot list file
cat > shot_list.md << 'EOF'
# YouTube Short #1 Shot List
## "Can You Solve This Ancient Code?"

### Shot 1: Hook (0-3 seconds)
- **Visual:** Close-up of ancient scroll unrolling
- **Text Overlay:** "🧠 GENIUS TEST"
- **Animation:** Scroll unroll with parchment texture
- **Audio:** Mysterious ambient sound + whisper "Genius test..."

### Shot 2: Cipher Reveal (3-8 seconds)
- **Visual:** Large encrypted text "KHOOR" appears
- **Animation:** Letters materialize one by one with golden glow
- **Text Overlay:** "Decode this ancient message"
- **Audio:** Mystical chime for each letter

### Shot 3: Teaching Moment (8-15 seconds)
- **Visual:** Split screen showing alphabet wheel rotation
- **Animation:** A→D, B→E, C→F transformations
- **Text Overlay:** "Each letter shifts by 3"
- **Audio:** Educational tone, gentle background music

### Shot 4: Letter-by-Letter Reveal (15-25 seconds)
- **Visual:** K→H, H→E, O→L, O→L, R→O transformations
- **Animation:** Smooth morphing animations with particle effects
- **Text Overlay:** Step-by-step solving process
- **Audio:** Satisfying 'click' sounds for each transformation

### Shot 5: Victory Moment (25-28 seconds)
- **Visual:** "HELLO" appears with golden explosion effect
- **Animation:** Text grows with sparkle particles
- **Text Overlay:** "✨ HELLO ✨"
- **Audio:** Triumphant chord progression

### Shot 6: Call to Action (28-30 seconds)
- **Visual:** Clean modern interface preview
- **Animation:** Button pulse effect
- **Text Overlay:** "Get weekly puzzles 🧩 START SOLVING"
- **Audio:** Upbeat, motivational tone
EOF

# Create filming checklist
cat > filming_checklist.md << 'EOF'
# YouTube Short #1 Filming Checklist

## Pre-Production ✅
- [ ] Script finalized (30 seconds exact)
- [ ] Shot list reviewed
- [ ] Props gathered (ancient scroll prop, lighting setup)
- [ ] Camera angles planned (vertical 9:16 format)
- [ ] Audio tracks prepared

## Equipment Setup
- [ ] Camera: Vertical orientation (1080x1920 minimum)
- [ ] Lighting: Warm golden key light, soft fill light
- [ ] Audio: Clear microphone for voiceover
- [ ] Props: Parchment paper, golden lighting filters
- [ ] Computer: After Effects ready for post-production

## Filming Shots
- [ ] Shot 1: Close-up scroll unroll (3 takes)
- [ ] Shot 2: Cipher text reveal setup (green screen optional)
- [ ] Shot 3: Alphabet wheel demonstration
- [ ] Shot 4: Letter transformation sequences
- [ ] Shot 5: Victory celebration moment
- [ ] Shot 6: Clean CTA button interaction

## Post-Production
- [ ] Import footage to After Effects
- [ ] Apply provided AE expressions
- [ ] Add particle effects
- [ ] Color grading (warm, ancient feel)
- [ ] Audio mixing and timing
- [ ] Export vertical 1080x1920 MP4

## Final Review
- [ ] 30-second duration exactly
- [ ] Captions added for accessibility
- [ ] Thumbnail created (bright, eye-catching)
- [ ] Title optimized: "Can You Solve This Ancient Code? 🧠"
- [ ] Description includes call-to-action link
EOF

# Create production timeline
cat > production_timeline.md << 'EOF'
# YouTube Short #1 Production Timeline

## Day 1: Pre-Production (2-3 hours)
- **Morning:** Script review and shot planning
- **Afternoon:** Equipment setup and prop preparation
- **Evening:** Test shots and lighting adjustments

## Day 2: Filming (4-5 hours)
- **Morning (2 hours):** Film all 6 shots with multiple takes
- **Afternoon (3 hours):** Review footage, select best takes
- **Evening:** Begin After Effects setup

## Day 3: Post-Production (6-8 hours)
- **Morning (3 hours):** Edit timeline, add animations
- **Afternoon (3 hours):** Apply effects, color grading
- **Evening (2 hours):** Audio mixing, final render

## Day 4: Publishing (1-2 hours)
- **Morning:** Create thumbnail, optimize title
- **Afternoon:** Upload to YouTube, set premiere time
- **Evening:** Promote on social media

## Success Metrics to Track:
- Views in first 24 hours (target: 1,000+)
- Watch time percentage (target: 70%+)
- Comments asking for more puzzles
- Click-through rate to beta signup page
- New beta signups from video traffic
EOF

# Create technical specs file
cat > technical_specs.md << 'EOF'
# YouTube Short #1 Technical Specifications

## Video Specs
- **Resolution:** 1080x1920 (vertical)
- **Frame Rate:** 30fps
- **Duration:** 30 seconds exactly
- **Codec:** H.264, high quality
- **File Size:** Under 50MB for optimal upload

## Color Palette
- **Primary:** #8B4513 (Saddle Brown)
- **Secondary:** #FFD700 (Gold)
- **Background:** #F5DEB3 (Wheat/Parchment)
- **Accent:** #DEB887 (Burlywood)

## Typography
- **Headers:** Cinzel (serif, ancient feel)
- **Body:** Courier New (monospace, code-like)
- **Emphasis:** Bold weights with text shadows

## Audio Levels
- **Voiceover:** -6dB to -12dB
- **Music:** -18dB to -24dB
- **Sound Effects:** -12dB to -18dB
- **Master Output:** Peak at -3dB

## Animation Timings
- **Scroll Unroll:** 0-3s (ease-out curve)
- **Letter Reveals:** 3-8s (0.8s per letter)
- **Transformations:** 15-25s (1s per letter)
- **Victory Effect:** 25-28s (explosive reveal)
- **CTA Button:** 28-30s (pulsing animation)

## Export Settings (After Effects)
- **Composition:** 1080x1920, 30fps, 30s
- **Render Queue:** H.264, Maximum Quality
- **Audio:** 48kHz, 16-bit, Stereo
- **Format:** MP4 (YouTube optimized)
EOF

# Generate After Effects project structure
cat > after_effects_project.md << 'EOF'
# After Effects Project Structure

## Composition Setup
1. **New Composition:** "YouTube_Short_1"
   - Width: 1080px, Height: 1920px
   - Frame Rate: 30fps, Duration: 30s

## Layer Organization
```
📁 MASTER COMP
├── 🎬 Shot_6_CTA (28-30s)
├── 🎬 Shot_5_Victory (25-28s)
├── 🎬 Shot_4_Transformations (15-25s)
├── 🎬 Shot_3_Teaching (8-15s)
├── 🎬 Shot_2_Cipher_Reveal (3-8s)
├── 🎬 Shot_1_Hook (0-3s)
├── 🎵 Audio_Master
├── 🌟 Particles_Global
└── 📜 Background_Scroll
```

## Pre-compositions Required
- **Scroll_Animation:** Parchment unroll effect
- **Letter_Morph:** Individual letter transformations
- **Particle_System:** Golden sparkle effects
- **Button_Pulse:** CTA button animation

## Essential Expressions
Copy the expressions from `after_effects_expressions.txt` for:
- Letter shifting animations
- Particle generation
- Scroll unroll physics
- Button pulse timing

## Rendering Pipeline
1. **Preview Render:** Half resolution for review
2. **Client Review:** Export as MP4 for feedback
3. **Final Render:** Full resolution for YouTube
4. **Backup:** Save project file and assets
EOF

echo "✅ Production files created successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Review shot_list.md for filming guidance"
echo "2. Follow filming_checklist.md during production"
echo "3. Use technical_specs.md for quality standards"
echo "4. Import after_effects_expressions.txt into AE"
echo ""
echo "🚀 Ready to film YouTube Short #1!"
echo "📱 Remember: Vertical format (9:16) for YouTube Shorts"
echo "⏱️  Target: Exactly 30 seconds for optimal algorithm performance"
