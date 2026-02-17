
import psycopg2
import os
from urllib.parse import urlparse

# User provided string, trying password without brackets
DB_URL = "postgresql://postgres.ijsbaxhpkqvxzyuwsptp:zbCskcVyycfu5MdR@aws-1-ap-south-1.pooler.supabase.com:6543/postgres"

def test_connection():
    print(f"Testing connection to: {DB_URL}")
    try:
        conn = psycopg2.connect(DB_URL)
        print("SUCCESS: Connected to Supabase!")
        conn.close()
    except Exception as e:
        print(f"ERROR: Connection failed.\n{e}")
        
        # DNS Debugging
        try:
            parsed = urlparse(DB_URL)
            hostname = parsed.hostname
            print(f"\nAttempting to resolve hostname: {hostname}")
            import socket
            ip = socket.gethostbyname(hostname)
            print(f"Hostname resolved to IP: {ip}")
        except Exception as dns_e:
            print(f"DNS Resolution failed: {dns_e}")

if __name__ == "__main__":
    test_connection()
