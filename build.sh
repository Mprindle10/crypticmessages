#!/bin/bash

# Build script for The Riddle Room - Netlify deployment
echo "🏛️ Building The Riddle Room for Netlify..."

# Create public directory
mkdir -p public

# Copy static HTML files to public directory
echo "📄 Copying static HTML files..."
cp beta_landing_page.html public/beta.html 2>/dev/null || echo "beta_landing_page.html not found"
cp beta_success.html public/success.html 2>/dev/null || echo "beta_success.html not found"
cp index.html public/index.html 2>/dev/null || echo "index.html not found"

# Copy any additional static files
cp -r *.css public/ 2>/dev/null || echo "No CSS files to copy"
cp -r *.js public/ 2>/dev/null || echo "No JS files to copy"

echo "✅ Static site build complete!"
echo "📁 Files in public directory:"
ls -la public/

echo "🚀 The Riddle Room is ready for deployment!"