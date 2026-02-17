
import psycopg2
import sys

project_id = "ijsbaxhpkqvxzyuwsptp"
password = "Gk4dH1a6UvveT3oT"
db_name = "postgres"

# List of common Supabase regions
regions = [
    "us-east-1", "us-east-2", "us-west-1", "us-west-2",
    "ap-south-1", "ap-northeast-1", "ap-northeast-2", "ap-southeast-1", "ap-southeast-2",
    "eu-central-1", "eu-west-1", "eu-west-2", "eu-west-3", "eu-north-1",
    "sa-east-1", "ca-central-1"
]

print(f"Searching for project {project_id} in {len(regions)} regions...")

for region in regions:
    pooler_host = f"aws-0-{region}.pooler.supabase.com"
    # Pooler typically uses port 6543, sometimes 5432. Session mode is 5432? Transaction is 6543?
    # Actually, Supavisor usually listens on 6543 for transaction mode and 5432 for session mode?
    # Docs say: port 6543 (transaction) or 5432 (session). 
    # But for the pooler hostname, it often requires a specific port.
    # Let's try port 6543 as it's the standard pooler port.
    
    # Connection string format for pooler:
    # postgres://[db_user].[project_ref]:[db_password]@[pooler_url]:6543/[db_name]
    
    dsn = f"postgresql://postgres.{project_id}:{password}@{pooler_host}:6543/{db_name}"
    
    print(f"Testing {region} ({pooler_host})...", end=" ")
    
    try:
        conn = psycopg2.connect(dsn, connect_timeout=3)
        print("SUCCESS! FOUND IT!")
        print(f"Region: {region}")
        print(f"Connection String: {dsn}")
        conn.close()
        break
    except psycopg2.OperationalError as e:
        msg = str(e).strip()
        if "Tenant or user not found" in msg:
            print("Not here (Tenant not found).")
        elif "network is unreachable" in msg.lower():
             print("Network unreachable (IPv6 issue?).")
        elif "could not translate host name" in msg:
            print("Hostname not found.")
        elif "password authentication failed" in msg:
            print("FOUND IT! (But password failed - project exists here).")
            print(f"Region: {region}")
            break
        else:
            print(f"Error: {msg}")
    except Exception as e:
        print(f"Unexpected error: {e}")
