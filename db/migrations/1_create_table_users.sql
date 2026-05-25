CREATE TABLE users (
    id_user SERIAL PRIMARY KEY,
    user_name VARCHAR(50) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    user_role VARCHAR(50) CHECK (user_role IN ('customer', 'importer', 'admin')) DEFAULT 'customer',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_users_user_name ON users(user_name);
