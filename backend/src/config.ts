import dotenv from 'dotenv';

dotenv.config();

export const config = {
    redis: {
        host: process.env.REDIS_HOST || 'localhost',
        port: parseInt(process.env.REDIS_PORT || '6379'),
    },
    postgres: {
        user: process.env.POSTGRES_USER || 'admin',
        host: process.env.POSTGRES_HOST || 'localhost',
        database: process.env.POSTGRES_DB || 'eylo_db',
        password: process.env.POSTGRES_PASSWORD || 'password',
        port: parseInt(process.env.POSTGRES_PORT || '5432'),
    },
    apify: {
        token: process.env.APIFY_TOKEN || 'mock_token',
    },
    gemini: {
        apiKey: process.env.GEMINI_API_KEY || 'mock_key',
    }
};
