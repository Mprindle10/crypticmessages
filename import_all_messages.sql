-- Complete Database Import Script for Cryptic Messages Subscription Service
-- This script imports all 273 messages for the 21-month "Cipher Academy Journey"

-- First, ensure the database and tables exist
\c theriddleroom;

-- Source the main table creation script
\i create_cryptic_messages_table.sql

-- Source the intermediate weeks (21-91)
\i complete_intermediate_weeks.sql

-- Verify the import
SELECT 
    COUNT(*) as total_messages,
    MIN(week_number) as first_week,
    MAX(week_number) as last_week,
    COUNT(DISTINCT week_number) as unique_weeks
FROM cryptic_messages;

-- Show message distribution by day
SELECT 
    day_of_week,
    COUNT(*) as message_count
FROM cryptic_messages
GROUP BY day_of_week
ORDER BY 
    CASE day_of_week 
        WHEN 'Sunday' THEN 1 
        WHEN 'Wednesday' THEN 2 
        WHEN 'Friday' THEN 3 
    END;

-- Show difficulty progression
SELECT 
    difficulty_level,
    COUNT(*) as message_count,
    MIN(week_number) as first_week,
    MAX(week_number) as last_week
FROM cryptic_messages
GROUP BY difficulty_level
ORDER BY difficulty_level;

-- Sample recent messages to verify content
SELECT 
    week_number,
    day_of_week,
    title,
    LEFT(message, 50) || '...' as message_preview,
    difficulty_level
FROM cryptic_messages 
WHERE week_number BETWEEN 85 AND 91
ORDER BY week_number, message_sequence;

-- Create admin view for monitoring
CREATE OR REPLACE VIEW message_overview AS
SELECT 
    week_number,
    day_of_week,
    message_sequence,
    title,
    difficulty_level,
    requires_previous_code,
    is_active,
    CASE 
        WHEN week_number <= 12 THEN 'Ancient Foundations'
        WHEN week_number <= 30 THEN 'Renaissance Revolution' 
        WHEN week_number <= 60 THEN 'Industrial Innovation'
        WHEN week_number <= 80 THEN 'Modern Warfare'
        ELSE 'Digital Future'
    END as era_category
FROM cryptic_messages
ORDER BY week_number, message_sequence;

-- Grant permissions for application user
GRANT SELECT, INSERT, UPDATE ON cryptic_messages TO app_user;
GRANT SELECT, INSERT, UPDATE ON user_submissions TO app_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON user_progress TO app_user;
GRANT SELECT ON message_overview TO app_user;

-- Final verification
\echo 'Database import completed successfully!'
\echo 'Total messages imported: '
SELECT COUNT(*) FROM cryptic_messages;
