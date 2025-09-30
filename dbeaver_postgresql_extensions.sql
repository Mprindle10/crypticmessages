-- PostgreSQL Extensions for Cryptic Message Service
-- Run these in DBeaver to enhance your database capabilities

-- 1. UUID Generation (for unique user IDs)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 2. Encryption (for sensitive user data)
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 3. Performance Monitoring
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";

-- 4. Text Search (for message content search)
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- 5. Fuzzy String Matching (for cipher similarity)
CREATE EXTENSION IF NOT EXISTS "fuzzystrmatch";

-- Example usage for your cryptic message service:

-- Generate secure user tokens
SELECT gen_random_uuid() as user_token;

-- Encrypt sensitive data
SELECT crypt('user_password', gen_salt('bf')) as encrypted_password;

-- Text similarity for cipher matching
SELECT similarity('CAESAR CIPHER', 'CESEAR CIPHER') as match_score;

-- Performance monitoring for your API queries
SELECT 
    query,
    calls,
    total_time,
    mean_time
FROM pg_stat_statements 
WHERE query LIKE '%cryptic_messages%'
ORDER BY total_time DESC
LIMIT 10;
