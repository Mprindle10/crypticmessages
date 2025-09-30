-- Migration: Add incorrect_attempts table for PATCH hint system
CREATE TABLE IF NOT EXISTS incorrect_attempts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    week_number INTEGER NOT NULL,
    puzzle_index INTEGER NOT NULL,
    attempt_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
