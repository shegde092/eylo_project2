import { Pool } from 'pg';
import dotenv from 'dotenv';

dotenv.config();

const pool = new Pool({
    user: process.env.POSTGRES_USER || 'admin',
    host: process.env.POSTGRES_HOST || 'localhost',
    database: process.env.POSTGRES_DB || 'eylo_db',
    password: process.env.POSTGRES_PASSWORD || 'password',
    port: parseInt(process.env.POSTGRES_PORT || '5432'),
});

export const query = (text: string, params?: any[]) => pool.query(text, params);
