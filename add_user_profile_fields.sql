-- Add additional user profile fields to users table
-- Migration for beta landing page form fields

ALTER TABLE users 
ADD COLUMN IF NOT EXISTS experience VARCHAR(100),
ADD COLUMN IF NOT EXISTS motivation TEXT,
ADD COLUMN IF NOT EXISTS background TEXT;

-- Create indexes for potential analytics queries
CREATE INDEX IF NOT EXISTS idx_users_experience ON users(experience);
CREATE INDEX IF NOT EXISTS idx_users_signup_source ON users(signup_source);

-- Update any existing users with default values
UPDATE users 
SET experience = 'not_specified'
WHERE experience IS NULL;

-- Add comments for documentation
COMMENT ON COLUMN users.experience IS 'User cryptography experience level (beginner, intermediate, advanced)';
COMMENT ON COLUMN users.motivation IS 'Why the user wants to learn cryptography';
COMMENT ON COLUMN users.background IS 'User professional/educational background';

COMMIT;
