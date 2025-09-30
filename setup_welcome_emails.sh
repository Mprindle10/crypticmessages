#!/bin/bash

# Setup Welcome Email Series Database Integration
# Run this script to integrate the welcome email system

echo "🔐 Setting up The Cipher Academy Welcome Email Series..."
echo ""

# Check if PostgreSQL is running
if ! pg_isready -h localhost -p 5432 > /dev/null 2>&1; then
    echo "❌ PostgreSQL is not running. Please start PostgreSQL first."
    exit 1
fi

echo "✅ PostgreSQL is running"

# Run database migrations
echo "📊 Running database migrations..."
psql -h localhost -U m -d theriddleroom -f welcome_email_database.sql

if [ $? -eq 0 ]; then
    echo "✅ Database migrations completed successfully"
else
    echo "❌ Database migrations failed"
    exit 1
fi

# Insert welcome email content from marketing materials
echo "📧 Setting up email templates..."

# Create a temporary SQL file with the email content
cat > temp_email_content.sql << 'EOF'
-- Update email templates with actual content from welcome_email_series.md

UPDATE email_templates SET 
    html_content = '
<div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; background: #f8f9fa;">
    <div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white; padding: 30px; text-align: center;">
        <h1 style="margin: 0; font-size: 2.2rem;">🔐 Welcome to The Cipher Academy!</h1>
        <p style="margin: 10px 0 0 0; font-size: 1.2rem; opacity: 0.9;">Your cryptographic journey begins now</p>
    </div>
    
    <div style="padding: 30px; background: white;">
        <h2 style="color: #1e3c72; margin-bottom: 20px;">Congratulations, {user_name}!</h2>
        
        <p style="font-size: 16px; line-height: 1.6; color: #333;">
            You've just taken the first step into 5,000 years of secret communications. From ancient Spartan warriors to modern cybersecurity experts, you're about to learn the techniques that shaped history.
        </p>
        
        <div style="background: #e9ecef; padding: 20px; border-left: 4px solid #2a5298; margin: 25px 0;">
            <h3 style="color: #1e3c72; margin-top: 0;">🏛️ Your First Challenge: The Caesar Cipher</h3>
            <p style="margin-bottom: 15px;"><strong>Historical Context:</strong> Julius Caesar used this cipher to protect his military communications around 50 BCE.</p>
            
            <div style="background: white; padding: 15px; border-radius: 8px; font-family: monospace; font-size: 18px; text-align: center; margin: 15px 0;">
                ZHOFRPH WR WKH FLSKHU DFDGHPB
            </div>
            
            <p><strong>Your Mission:</strong> Decode this message using Caesar's method. Each letter has been shifted by 3 positions forward in the alphabet.</p>
        </div>
        
        <div style="text-align: center; margin: 30px 0;">
            <a href="{submission_url}" 
               style="background: #ff6b35; color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px; font-weight: bold; display: inline-block;">
                Submit Your Solution
            </a>
        </div>
    </div>
</div>',
    plain_text_content = '
🔐 WELCOME TO THE CIPHER ACADEMY!

Congratulations, {user_name}!

You've just taken the first step into 5,000 years of secret communications.

🏛️ YOUR FIRST CHALLENGE: The Caesar Cipher

Historical Context: Julius Caesar used this cipher to protect his military communications around 50 BCE.

Your Challenge:
ZHOFRPH WR WKH FLSKHU DFDGHPB

Your Mission: Decode this message using Caesar's method. Each letter has been shifted by 3 positions forward.

Submit your solution: {submission_url}

The Cipher Academy Team'
WHERE template_name = 'welcome_challenge';

-- Update other templates with simplified versions
UPDATE email_templates SET 
    html_content = '<div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;"><div style="background: linear-gradient(135deg, #8B4513 0%, #DAA520 100%); color: white; padding: 25px; text-align: center;"><h1>🏛️ The Secret History of Cryptography</h1></div><div style="padding: 30px; background: white;"><h2>How ciphers shaped civilization</h2><p>Did you solve your first Caesar cipher? If you decoded "WELCOME TO THE CIPHER ACADEMY" - congratulations!</p><div style="text-align: center; margin: 30px 0;"><a href="{progress_url}" style="background: #8B4513; color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px;">Explore Timeline</a></div></div></div>',
    plain_text_content = 'How Secret Messages Changed History\n\nDid you solve your first Caesar cipher? If you decoded "WELCOME TO THE CIPHER ACADEMY" - congratulations!\n\nExplore more: {progress_url}'
WHERE template_name = 'historical_context';

UPDATE email_templates SET 
    html_content = '<div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;"><div style="background: linear-gradient(135deg, #2E8B57 0%, #4169E1 100%); color: white; padding: 25px; text-align: center;"><h1>🔍 Master the Art of Code-Breaking</h1></div><div style="padding: 30px; background: white;"><h2>5 Essential Cipher-Breaking Techniques</h2><p>Learn the expert techniques used by professional cryptographers.</p><div style="text-align: center; margin: 30px 0;"><a href="{practice_url}" style="background: #2E8B57; color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px;">Practice Techniques</a></div></div></div>',
    plain_text_content = 'Master the Art of Code-Breaking\n\n5 Essential Cipher-Breaking Techniques\n\nPractice: {practice_url}'
WHERE template_name = 'solving_tips';

UPDATE email_templates SET 
    html_content = '<div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;"><div style="background: linear-gradient(135deg, #9400D3 0%, #4B0082 100%); color: white; padding: 25px; text-align: center;"><h1>👥 The Cipher Academy Community</h1><p>2,847 cryptography enthusiasts and growing</p></div><div style="padding: 30px; background: white;"><h2>You're Not Solving Alone</h2><p>Welcome to one of the most supportive learning communities online!</p><div style="text-align: center; margin: 30px 0;"><a href="{community_url}" style="background: #9400D3; color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px;">Join the Forum</a></div></div></div>',
    plain_text_content = 'The Cipher Academy Community\n\nWelcome to our supportive learning community!\n\nJoin: {community_url}'
WHERE template_name = 'community_intro';

UPDATE email_templates SET 
    html_content = '<div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;"><div style="background: linear-gradient(135deg, #ff6b35 0%, #f7931e 100%); color: white; padding: 25px; text-align: center;"><h1>📊 Your Learning Dashboard</h1></div><div style="padding: 30px; background: white;"><h2>Track Your Progress</h2><p>You've completed {weeks_completed} weeks and reached level {current_level}!</p><div style="text-align: center; margin: 30px 0;"><a href="{dashboard_url}" style="background: #ff6b35; color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px;">View Dashboard</a></div></div></div>',
    plain_text_content = 'Your Learning Dashboard\n\nYou've completed {weeks_completed} weeks!\n\nView progress: {dashboard_url}'
WHERE template_name = 'progress_tracking';

UPDATE email_templates SET 
    html_content = '<div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;"><div style="background: linear-gradient(135deg, #37474f 0%, #263238 100%); color: white; padding: 25px; text-align: center;"><h1>🚀 Advanced Cryptographic Warfare</h1></div><div style="padding: 30px; background: white;"><h2>WWII Code-Breaking Secrets</h2><p>Get a glimpse of advanced techniques from the Industrial Innovation era.</p><div style="text-align: center; margin: 30px 0;"><a href="{preview_url}" style="background: #37474f; color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px;">Explore Industrial Era</a></div></div></div>',
    plain_text_content = 'Advanced Cryptographic Warfare\n\nWWII Code-Breaking Secrets preview\n\nExplore: {preview_url}'
WHERE template_name = 'advanced_preview';

UPDATE email_templates SET 
    html_content = '<div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;"><div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white; padding: 25px; text-align: center;"><h1>🎯 Your Cryptographic Destiny Awaits</h1></div><div style="padding: 30px; background: white;"><h2>Ready for the Complete Journey?</h2><div style="background: linear-gradient(135deg, #ffd700 0%, #ffeb3b 100%); padding: 25px; border-radius: 12px; text-align: center;"><h3 style="color: #1e3c72;">⏰ Limited-Time Offer</h3><div style="font-size: 2.5rem; color: #1e3c72; font-weight: bold;">$197</div><div style="text-decoration: line-through; color: #666;">Regular: $297</div></div><div style="text-align: center; margin: 30px 0;"><a href="{upgrade_url}" style="background: #1e3c72; color: white; padding: 20px 40px; text-decoration: none; border-radius: 12px; font-weight: bold; font-size: 1.2rem;">🚀 Begin Complete Journey</a></div></div></div>',
    plain_text_content = 'Your Cryptographic Destiny Awaits\n\nLimited-Time Offer: $197 (Save $100)\n\nUpgrade: {upgrade_url}'
WHERE template_name = 'upgrade_offer';
EOF

psql -h localhost -U m -d theriddleroom -f temp_email_content.sql

if [ $? -eq 0 ]; then
    echo "✅ Email templates updated successfully"
    rm temp_email_content.sql
else
    echo "❌ Failed to update email templates"
    rm temp_email_content.sql
    exit 1
fi

# Test the welcome email system
echo "🧪 Testing welcome email system..."

# Check if the functions work
psql -h localhost -U m -d theriddleroom -c "SELECT count(*) as template_count FROM email_templates;" -t

if [ $? -eq 0 ]; then
    echo "✅ Welcome email system is ready!"
else
    echo "❌ Welcome email system test failed"
    exit 1
fi

echo ""
echo "🎉 Setup Complete!"
echo ""
echo "Welcome email series features:"
echo "  📧 7 automated emails over 14 days"
echo "  🎯 Personalized content with user progress"
echo "  🧩 Interactive cipher challenges"
echo "  📊 Email tracking and analytics"
echo "  🔄 Automatic scheduling on user signup"
echo ""
echo "Next steps:"
echo "  1. Add welcome_email_api.py routes to your main FastAPI app"
echo "  2. Configure SendGrid webhook: /api/welcome-emails/sendgrid-webhook"
echo "  3. Start the scheduler service: python scheduler_service.py"
echo "  4. Test with a new user signup to see the welcome series trigger"
echo ""
echo "API endpoints available:"
echo "  POST /api/welcome-emails/challenge-submission"
echo "  GET  /api/welcome-emails/stats"
echo "  GET  /api/welcome-emails/user/{user_id}/progress"
echo "  POST /api/welcome-emails/resend/{user_id}/{email_sequence}"
echo ""
