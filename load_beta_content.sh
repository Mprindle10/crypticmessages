#!/bin/bash
# Load Beta Content into Cipher Academy Database

echo "🔐 Loading Beta Week 1 Content into Database..."

# Source environment variables
source .venv/bin/activate
export $(grep -v '^#' .env | xargs)

# Connect to PostgreSQL and insert beta content
psql -U m -d theriddleroom << 'EOF'

-- Clear any existing Week 1 content (for beta testing)
DELETE FROM cryptic_messages WHERE week_number = 1;

-- Insert Week 1 Beta Challenges
INSERT INTO cryptic_messages (week_number, day_of_week, title, content, answer, difficulty_level, points_value, hint, cipher_type, created_at) VALUES
(1, 'Sunday', 'Caesar''s First Message', 'WKLV LV MXVW WKH EHJLQQLQJ', 'THIS IS JUST THE BEGINNING', 1, 10, 'Caesar shift of 3: A→D, B→E, C→F', 'Caesar Cipher', NOW()),
(1, 'Wednesday', 'Military Dispatch', 'DWWDFN DW GDZQ', 'ATTACK AT DAWN', 1, 10, 'Same shift as Sunday. Pattern recognition from previous solution.', 'Caesar Cipher', NOW()),
(1, 'Friday', 'Secret Rendezvous', 'PHHW DW WKH IRUXP', 'MEET AT THE FORUM', 1, 15, 'Same Caesar shift. Think about Roman gathering places.', 'Caesar Cipher', NOW());

-- Insert beta email templates
INSERT INTO email_templates (template_name, email_sequence, subject_line, html_content, plain_text_content, days_after_signup, is_active) VALUES
('beta_welcome', 1, 'Welcome to Cipher Academy - Your First Mission Awaits 🔐', 
'<h1>Welcome, Cryptographer!</h1><p>Your first challenge: WKLV LV MXVW WKH EHJLQQLQJ</p>', 
'Welcome, Cryptographer! Your first challenge: WKLV LV MXVW WKH EHJLQQLQJ', 
0, true),
('beta_progress_check', 2, 'How''s Your First Cipher Going? 🤔', 
'<h1>Progress Check</h1><p>Need help with Caesar''s cipher?</p>', 
'Progress Check: Need help with Caesar''s cipher?', 
3, true),
('beta_feedback', 3, 'Help Shape the Future of Cipher Academy 🛠️', 
'<h1>Your Feedback Matters</h1><p>Complete our beta survey.</p>', 
'Your Feedback Matters: Complete our beta survey.', 
7, true);

-- Create beta user tracking
CREATE TABLE IF NOT EXISTS beta_feedback (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    week_number INTEGER,
    feedback_type VARCHAR(50), -- 'difficulty', 'timing', 'content', 'technical'
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    comments TEXT,
    submitted_at TIMESTAMP DEFAULT NOW()
);

-- Create beta subscription plan
INSERT INTO subscription_plans (plan_name, price_cents, interval_months, description, features) VALUES
('beta_trial', 0, 1, 'Beta Trial - Free First Month', '["Free first month", "50% lifetime discount", "Direct founder access", "Founding member badge"]')
ON CONFLICT (plan_name) DO NOTHING;

-- Verify content loaded
SELECT 'Week 1 Challenges Loaded:' as status, count(*) as challenge_count FROM cryptic_messages WHERE week_number = 1;
SELECT 'Email Templates Loaded:' as status, count(*) as template_count FROM email_templates WHERE template_name LIKE 'beta_%';

EOF

echo "✅ Beta content loaded successfully!"
echo ""
echo "🎯 Next Steps:"
echo "1. Start your FastAPI server: uvicorn main:app --reload"
echo "2. Open beta landing page: http://localhost:8000/beta"  
echo "3. Test beta signup process"
echo "4. Begin recruiting your 50 beta testers!"
echo ""
echo "🚀 Ready to launch your cryptographic revolution!"
