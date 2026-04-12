from google.cloud import bigquery
from pathlib import Path

client = bigquery.Client(project="o9-dashboard-493005")

client.query(
    "CREATE SCHEMA IF NOT EXISTS `o9-dashboard-493005.dev_staging` OPTIONS (location = 'asia-southeast3')"
    , job_config=bigquery.QueryJobConfig(),
    location="asia-southeast3"
).result()
print("Dataset dev_staging ready.")

for sql_file in sorted(Path("sql/staging/").glob("stg_*.sql")):
    sql = sql_file.read_text()
    print(f"Deploying {sql_file.name}...")
    client.query(sql, location="asia-southeast3").result()
    print(f"  done: {sql_file.name}")

print("\nAll staging views deployed!")