-- Fix users table to match the User model
-- Add missing columns for subscription service

ALTER TABLE users 
ADD COLUMN IF NOT EXISTS subscription_type character varying(50) DEFAULT 'free_trial',
ADD COLUMN IF NOT EXISTS signup_source character varying(100),
ADD COLUMN IF NOT EXISTS created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN IF NOT EXISTS current_week integer DEFAULT 1,
ADD COLUMN IF NOT EXISTS total_points integer DEFAULT 0,
ADD COLUMN IF NOT EXISTS current_streak integer DEFAULT 0,
ADD COLUMN IF NOT EXISTS subscription_id character varying(255);

-- Update existing NULL values to defaults
UPDATE users SET 
    subscription_type = 'free_trial' WHERE subscription_type IS NULL,
    current_week = 1 WHERE current_week IS NULL,
    total_points = 0 WHERE total_points IS NULL,
    current_streak = 0 WHERE current_streak IS NULL,
    created_at = CURRENT_TIMESTAMP WHERE created_at IS NULL;

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_subscription_type ON users(subscription_type);
CREATE INDEX IF NOT EXISTS idx_users_signup_source ON users(signup_source);
CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at);
