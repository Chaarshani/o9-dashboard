from google.cloud import bigquery
client = bigquery.Client(project="o9-dashboard-493005", location="asia-southeast3")

sql = """
SELECT 
    go_live,
    actual_golive,
    blueprint_start,
    first_start_date_original
FROM `o9-dashboard-493005.dev_raw.raw_go_lives`
LIMIT 5
"""
for row in client.query(sql, location="asia-southeast3").result():
    print(f"go_live: '{row.go_live}' | actual_golive: '{row.actual_golive}' | blueprint_start: '{row.blueprint_start}' | first_start_date_original: '{row.first_start_date_original}'")