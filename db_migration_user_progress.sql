-- Migration: Add user_progress table
CREATE TABLE IF NOT EXISTS user_progress (
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    current_week INTEGER NOT NULL,
    last_answer TEXT,
    current_layer INTEGER NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id)
);
