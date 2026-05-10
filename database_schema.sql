-- Database Schema for Smart Task Manager

-- Users Table
CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password_hash VARCHAR(200) NOT NULL
);

-- Tasks Table
CREATE TABLE task (
    id SERIAL PRIMARY KEY,
    title VARCHAR(120) NOT NULL,
    desc VARCHAR(500) NOT NULL,
    priority VARCHAR(8) DEFAULT 'LOW',
    status VARCHAR(20) DEFAULT 'Pending',
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES "user" (id) ON DELETE CASCADE
);
