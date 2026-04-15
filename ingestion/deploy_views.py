from google.cloud import bigquery
from pathlib import Path

client = bigquery.Client(project="o9-dashboard-493005", location="asia-southeast3")

for sql_file in sorted(Path("sql/views/").glob("vw_*.sql")):
    sql = sql_file.read_text()
    print(f"Deploying {sql_file.name}...")
    client.query(sql, location="asia-southeast3").result()
    print(f"  done: {sql_file.name}")

print("\nAll views deployed!")