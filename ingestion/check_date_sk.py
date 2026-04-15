from google.cloud import bigquery
client = bigquery.Client(project="o9-dashboard-493005", location="asia-southeast3")

print("=== raw_advocacy time__calendar_month_ sample ===")
for r in client.query(
    "SELECT DISTINCT time__calendar_month_ FROM `o9-dashboard-493005.dev_raw.raw_advocacy` LIMIT 5",
    location="asia-southeast3"
).result():
    print(f"  '{r.time__calendar_month_}'")

print("=== raw_client_health time__calendar_month_ sample ===")
for r in client.query(
    "SELECT DISTINCT time__calendar_month_ FROM `o9-dashboard-493005.dev_raw.raw_client_health` LIMIT 5",
    location="asia-southeast3"
).result():
    print(f"  '{r.time__calendar_month_}'")