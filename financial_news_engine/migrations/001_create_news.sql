CREATE TABLE IF NOT EXISTS news (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    summary TEXT,
    url TEXT NOT NULL UNIQUE,
    source TEXT NOT NULL,
    published TIMESTAMPTZ NOT NULL,
    sentiment FLOAT,
    label TEXT,
    entities TEXT[],
    topic TEXT
);

CREATE INDEX IF NOT EXISTS idx_news_published ON news (published DESC);
CREATE INDEX IF NOT EXISTS idx_news_source ON news (source);
