-- Welcome Email Series Database Integration
-- Add to existing db_schema.sql

-- Email templates table for storing reusable email content
CREATE TABLE IF NOT EXISTS email_templates (
    id SERIAL PRIMARY KEY,
    template_name VARCHAR(100) UNIQUE NOT NULL,
    subject VARCHAR(255) NOT NULL,
    html_content TEXT NOT NULL,
    plain_text_content TEXT NOT NULL,
    template_variables JSONB, -- Store template variable definitions
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Welcome email series configuration
CREATE TABLE IF NOT EXISTS welcome_email_series (
    id SERIAL PRIMARY KEY,
    email_sequence INTEGER NOT NULL, -- 1-7 for the 7 emails
    delay_hours INTEGER NOT NULL, -- Hours after signup to send
    template_id INTEGER REFERENCES email_templates(id),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User welcome email tracking
CREATE TABLE IF NOT EXISTS user_welcome_emails (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    email_sequence INTEGER NOT NULL,
    scheduled_at TIMESTAMP NOT NULL,
    sent_at TIMESTAMP,
    opened_at TIMESTAMP,
    clicked_at TIMESTAMP,
    status VARCHAR(50) DEFAULT 'scheduled', -- scheduled, sent, delivered, opened, clicked, failed
    sendgrid_message_id VARCHAR(255),
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(user_id, email_sequence) -- Prevent duplicate emails
);

-- User email preferences
CREATE TABLE IF NOT EXISTS user_email_preferences (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) UNIQUE,
    welcome_series_enabled BOOLEAN DEFAULT TRUE,
    marketing_emails_enabled BOOLEAN DEFAULT TRUE,
    challenge_emails_enabled BOOLEAN DEFAULT TRUE,
    community_emails_enabled BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Challenge submissions for email series
CREATE TABLE IF NOT EXISTS email_challenge_submissions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    email_sequence INTEGER NOT NULL,
    challenge_type VARCHAR(50), -- 'caesar', 'atbash', 'polybius', etc.
    submitted_solution TEXT,
    is_correct BOOLEAN,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX(user_id, email_sequence)
);

-- Insert welcome email series configuration
    INSERT INTO welcome_email_series (email_sequence, delay_hours,
(7, 336, TRUE);  -- Day 14

-- Insert email templates
INSERT INTO email_templates (template_name, subject, html_content, plain_text_content, template_variables) VALUES
('welcome_challenge', 
 '🔐 Welcome to The Cipher Academy - Your First Challenge Awaits!',
 '<!-- HTML content from welcome_email_series.md Email 1 -->',
 'Plain text content from welcome_email_series.md Email 1',
 '{"user_name": "string", "challenge_code": "string", "submission_url": "string"}'::jsonb),

('historical_context',
 '🏛️ How Secret Messages Changed the Course of History',
 '<!-- HTML content from welcome_email_series.md Email 2 -->',
 'Plain text content from welcome_email_series.md Email 2',
 '{"user_name": "string", "progress_url": "string"}'::jsonb),

('solving_tips',
 '🔍 Cipher-Breaking Secrets: 5 Expert Tips for Beginners',
 '<!-- HTML content from welcome_email_series.md Email 3 -->',
 'Plain text content from welcome_email_series.md Email 3',
 '{"user_name": "string", "practice_challenge": "string", "practice_url": "string"}'::jsonb),

('community_intro',
 '👥 Meet Your Fellow Code-Breakers - Welcome to the Community!',
 '<!-- HTML content from welcome_email_series.md Email 4 -->',
 'Plain text content from welcome_email_series.md Email 4',
 '{"user_name": "string", "community_url": "string", "discord_url": "string", "weekly_challenge": "string"}'::jsonb),

('progress_tracking',
 '📊 Track Your Cryptographic Journey - Progress Dashboard Tutorial',
 '<!-- HTML content from welcome_email_series.md Email 5 -->',
 'Plain text content from welcome_email_series.md Email 5',
 '{"user_name": "string", "dashboard_url": "string", "weeks_completed": "number", "current_level": "number"}'::jsonb),

('advanced_preview',
 '🚀 WWII Code-Breaking Secrets - Advanced Techniques Preview',
 '<!-- HTML content from welcome_email_series.md Email 6 -->',
 'Plain text content from welcome_email_series.md Email 6',
 '{"user_name": "string", "preview_url": "string", "enigma_challenge": "string"}'::jsonb),

('upgrade_offer',
 '🎯 Ready for the Complete Journey? Special Launch Offer Inside',
 '<!-- HTML content from welcome_email_series.md Email 7 -->',
 'Plain text content from welcome_email_series.md Email 7',
 '{"user_name": "string", "upgrade_url": "string", "offer_price": "string", "expires_at": "string", "spots_remaining": "number"}'::jsonb);

-- Create indexes for performance
CREATE INDEX idx_user_welcome_emails_user_id ON user_welcome_emails(user_id);
CREATE INDEX idx_user_welcome_emails_scheduled_at ON user_welcome_emails(scheduled_at);
CREATE INDEX idx_user_welcome_emails_status ON user_welcome_emails(status);
CREATE INDEX idx_email_challenge_submissions_user_id ON email_challenge_submissions(user_id);

-- Function to automatically schedule welcome emails when user signs up
CREATE OR REPLACE FUNCTION schedule_welcome_emails()
RETURNS TRIGGER AS $$
BEGIN
    -- Insert all 7 welcome emails for the new user
    INSERT INTO user_welcome_emails (user_id, email_sequence, scheduled_at, status)
    SELECT 
        NEW.id,
        wes.email_sequence,
        NEW.created_at + INTERVAL '1 hour' * wes.delay_hours,
        'scheduled'
    FROM welcome_email_series wes
    WHERE wes.is_active = TRUE;
    
    -- Insert default email preferences
    INSERT INTO user_email_preferences (user_id)
    VALUES (NEW.id)
    ON CONFLICT (user_id) DO NOTHING;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to automatically schedule welcome emails on user signup
CREATE TRIGGER trigger_schedule_welcome_emails
    AFTER INSERT ON users
    FOR EACH ROW
    EXECUTE FUNCTION schedule_welcome_emails();

-- Function to get pending welcome emails (for scheduler)
CREATE OR REPLACE FUNCTION get_pending_welcome_emails()
RETURNS TABLE (
    user_id INTEGER,
    email VARCHAR(255),
    email_sequence INTEGER,
    template_name VARCHAR(100),
    subject VARCHAR(255),
    html_content TEXT,
    plain_text_content TEXT,
    template_variables JSONB,
    scheduled_id INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        u.id,
        u.email,
        uwe.email_sequence,
        et.template_name,
        et.subject,
        et.html_content,
        et.plain_text_content,
        et.template_variables,
        uwe.id as scheduled_id
    FROM user_welcome_emails uwe
    JOIN users u ON u.id = uwe.user_id
    JOIN welcome_email_series wes ON wes.email_sequence = uwe.email_sequence
    JOIN email_templates et ON et.id = wes.template_id
    JOIN user_email_preferences uep ON uep.user_id = u.id
    WHERE uwe.status = 'scheduled'
        AND uwe.scheduled_at <= CURRENT_TIMESTAMP
        AND u.is_active = TRUE
        AND uep.welcome_series_enabled = TRUE
    ORDER BY uwe.scheduled_at ASC;
END;
$$ LANGUAGE plpgsql;

-- Function to mark welcome email as sent
CREATE OR REPLACE FUNCTION mark_welcome_email_sent(
    scheduled_id INTEGER,
    sendgrid_message_id VARCHAR(255)
)
RETURNS VOID AS $$
BEGIN
    UPDATE user_welcome_emails 
    SET 
        status = 'sent',
        sent_at = CURRENT_TIMESTAMP,
        sendgrid_message_id = sendgrid_message_id
    WHERE id = scheduled_id;
END;
$$ LANGUAGE plpgsql;

-- Function to track email events (opens, clicks)
CREATE OR REPLACE FUNCTION track_welcome_email_event(
    sendgrid_msg_id VARCHAR(255),
    event_type VARCHAR(50),
    event_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
RETURNS VOID AS $$
BEGIN
    CASE event_type
        WHEN 'open' THEN
            UPDATE user_welcome_emails 
            SET opened_at = event_timestamp
            WHERE sendgrid_message_id = sendgrid_msg_id;
            
        WHEN 'click' THEN
            UPDATE user_welcome_emails 
            SET clicked_at = event_timestamp
            WHERE sendgrid_message_id = sendgrid_msg_id;
            
        WHEN 'delivered' THEN
            UPDATE user_welcome_emails 
            SET status = 'delivered'
            WHERE sendgrid_message_id = sendgrid_msg_id;
    END CASE;
END;
$$ LANGUAGE plpgsql;
