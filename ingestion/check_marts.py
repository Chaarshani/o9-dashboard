from google.cloud import bigquery
client = bigquery.Client(project="o9-dashboard-493005", location="asia-southeast3")

tables = [
    "dev_marts.dim_customer",
    "dev_marts.dim_project",
    "dev_marts.dim_date",
    "dev_marts.fct_financials",
    "dev_marts.fct_client_health",
    "dev_marts.fct_advocacy",
    "dev_marts.fct_go_lives",
]

for t in tables:
    result = client.query(
        f"SELECT COUNT(*) as cnt FROM `o9-dashboard-493005.{t}`",
        location="asia-southeast3"
    ).result()
    for row in result:
        print(f"{t}: {row.cnt} rows")
