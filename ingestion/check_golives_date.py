from google.cloud import bigquery
client = bigquery.Client(project="o9-dashboard-493005", location="asia-southeast3")

# Check what date_sk values are in fct_go_lives
sql = """
SELECT 
    date_sk,
    actual_go_live,
    go_live_original,
    COUNT(*) as cnt
FROM `o9-dashboard-493005.dev_marts.fct_go_lives`
GROUP BY 1, 2, 3
ORDER BY 1
"""
print("=== fct_go_lives date_sk values ===")
for row in client.query(sql, location="asia-southeast3").result():
    print(f"  date_sk: {row.date_sk}, actual_go_live: {row.actual_go_live}, go_live_original: {row.go_live_original}")

# Check sample date_sk values in dim_date
sql2 = """
SELECT date_sk, date 
FROM `o9-dashboard-493005.dev_marts.dim_date` 
ORDER BY date_sk 
LIMIT 5
"""
print("\n=== dim_date sample date_sk values ===")
for row in client.query(sql2, location="asia-southeast3").result():
    print(f"  date_sk: {row.date_sk}, date: {row.date}")