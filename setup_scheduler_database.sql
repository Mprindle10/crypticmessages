-- Create message_deliveries table for tracking
CREATE TABLE IF NOT EXISTS message_deliveries (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    week_number INTEGER NOT NULL,
    day_of_week VARCHAR(10) NOT NULL CHECK (day_of_week IN ('Sunday', 'Wednesday', 'Friday')),
    message_sequence INTEGER NOT NULL,
    delivered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    delivery_method VARCHAR(20) DEFAULT 'sms_email',
    delivery_status VARCHAR(20) DEFAULT 'success',
    UNIQUE(user_id, week_number, day_of_week)
);

-- Create indexes for delivery tracking
CREATE INDEX IF NOT EXISTS idx_message_deliveries_user_week ON message_deliveries(user_id, week_number);
CREATE INDEX IF NOT EXISTS idx_message_deliveries_delivered_at ON message_deliveries(delivered_at);

-- Add users table fields needed for scheduling (if not exists)
ALTER TABLE users ADD COLUMN IF NOT EXISTS phone_number VARCHAR(20);
ALTER TABLE users ADD COLUMN IF NOT EXISTS email VARCHAR(255);
ALTER TABLE users ADD COLUMN IF NOT EXISTS subscription_status VARCHAR(20) DEFAULT 'active';
ALTER TABLE users ADD COLUMN IF NOT EXISTS subscription_start_date DATE DEFAULT CURRENT_DATE;
ALTER TABLE users ADD COLUMN IF NOT EXISTS subscription_end_date DATE;
ALTER TABLE users ADD COLUMN IF NOT EXISTS timezone VARCHAR(50) DEFAULT 'UTC';
ALTER TABLE users ADD COLUMN IF NOT EXISTS preferred_delivery_method VARCHAR(20) DEFAULT 'both';

-- Create notification preferences table
CREATE TABLE IF NOT EXISTS notification_preferences (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE UNIQUE,
    sms_enabled BOOLEAN DEFAULT true,
    email_enabled BOOLEAN DEFAULT true,
    sunday_time TIME DEFAULT '08:00:00',
    wednesday_time TIME DEFAULT '18:00:00',
    friday_time TIME DEFAULT '15:00:00',
    timezone VARCHAR(50) DEFAULT 'UTC',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create scheduler status table for monitoring
CREATE TABLE IF NOT EXISTS scheduler_status (
    id SERIAL PRIMARY KEY,
    service_name VARCHAR(50) NOT NULL,
    last_run_at TIMESTAMP,
    next_run_at TIMESTAMP,
    status VARCHAR(20) DEFAULT 'active',
    messages_sent INTEGER DEFAULT 0,
    errors_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert initial scheduler status
INSERT INTO scheduler_status (service_name, status, created_at) 
VALUES ('cryptic_message_scheduler', 'active', CURRENT_TIMESTAMP)
ON CONFLICT (service_name) DO NOTHING;

-- Create function to update user progress after successful deliveries
CREATE OR REPLACE FUNCTION advance_user_week()
RETURNS TRIGGER AS $$
BEGIN
    -- Check if user completed all three messages for the week
    IF (SELECT COUNT(*) FROM user_submissions us 
        WHERE us.user_id = NEW.user_id 
        AND us.week_number = NEW.week_number 
        AND us.is_correct = true) = 3 THEN
        
        -- Advance to next week
        UPDATE user_progress 
        SET current_week = current_week + 1,
            updated_at = CURRENT_TIMESTAMP
        WHERE user_id = NEW.user_id;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger for automatic week advancement
CREATE TRIGGER trigger_advance_user_week
    AFTER INSERT ON user_submissions
    FOR EACH ROW
    WHEN (NEW.is_correct = true)
    EXECUTE FUNCTION advance_user_week();

-- Create view for scheduler monitoring
CREATE OR REPLACE VIEW delivery_analytics AS
SELECT 
    d.week_number,
    d.day_of_week,
    COUNT(*) as total_deliveries,
    COUNT(DISTINCT d.user_id) as unique_users,
    d.delivered_at::date as delivery_date,
    AVG(EXTRACT(EPOCH FROM (us.completed_at - d.delivered_at))/3600) as avg_solve_time_hours
FROM message_deliveries d
LEFT JOIN user_submissions us ON (
    d.user_id = us.user_id AND 
    d.week_number = us.week_number AND 
    d.day_of_week = us.day_of_week AND
    us.is_correct = true
)
GROUP BY d.week_number, d.day_of_week, d.delivered_at::date
ORDER BY delivery_date DESC, d.week_number, 
    CASE d.day_of_week 
        WHEN 'Sunday' THEN 1 
        WHEN 'Wednesday' THEN 2 
        WHEN 'Friday' THEN 3 
    END;

-- Grant permissions
GRANT SELECT, INSERT, UPDATE ON message_deliveries TO app_user;
GRANT SELECT, INSERT, UPDATE ON notification_preferences TO app_user;
GRANT SELECT, UPDATE ON scheduler_status TO app_user;
GRANT SELECT ON delivery_analytics TO app_user;
