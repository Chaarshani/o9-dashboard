from google.cloud import bigquery
from pathlib import Path

client = bigquery.Client(project="o9-dashboard-493005", location="asia-southeast3")

# Create dataset
dataset = bigquery.Dataset("o9-dashboard-493005.dev_marts")
dataset.location = "asia-southeast3"
client.create_dataset(dataset, exists_ok=True)
print("Dataset dev_marts ready.")

# Deploy dims first (facts depend on them)
for folder, label in [("sql/dims/", "dim"), ("sql/facts/", "fct")]:
    for sql_file in sorted(Path(folder).glob("*.sql")):
        sql = sql_file.read_text()
        print(f"Deploying {sql_file.name}...")
        client.query(sql, location="asia-southeast3").result()
        print(f"  done: {sql_file.name}")

print("\nAll mart tables deployed!")