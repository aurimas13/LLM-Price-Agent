-- sql/setup.sql
CREATE EXTENSION IF NOT EXISTS pgvector;
CREATE TABLE IF NOT EXISTS product_vectors (
    id SERIAL PRIMARY KEY,
    title TEXT,
    description TEXT,
    vector VECTOR(384)
);

