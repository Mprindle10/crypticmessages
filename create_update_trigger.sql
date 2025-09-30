-- Database Update Trigger for cryptic_messages table
-- This creates an automatic timestamp update trigger

-- First, create the function to update the updated_at column
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create the trigger on cryptic_messages table
DROP TRIGGER IF EXISTS update_cryptic_messages_updated_at ON cryptic_messages;

CREATE TRIGGER update_cryptic_messages_updated_at
    BEFORE UPDATE ON cryptic_messages
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Verify the trigger was created
SELECT 
    trigger_name,
    event_manipulation,
    event_object_table,
    action_timing,
    action_statement
FROM information_schema.triggers 
WHERE event_object_table = 'cryptic_messages';

-- Test the trigger with a sample update
SELECT 'Trigger created successfully for cryptic_messages table' AS status;
