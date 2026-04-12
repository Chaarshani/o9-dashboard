from google.cloud import bigquery
client = bigquery.Client(project="o9-dashboard-493005", location="asia-southeast3")

checks = {
    "fct_financials → dim_date": """
        SELECT COUNT(*) as unmatched FROM `o9-dashboard-493005.dev_marts.fct_financials` f
        LEFT JOIN `o9-dashboard-493005.dev_marts.dim_date` d ON f.date_sk = d.date_sk
        WHERE d.date_sk IS NULL
    """,
    "fct_financials → dim_customer": """
        SELECT COUNT(*) as unmatched FROM `o9-dashboard-493005.dev_marts.fct_financials` f
        LEFT JOIN `o9-dashboard-493005.dev_marts.dim_customer` c ON f.customer_sk = c.customer_sk
        WHERE c.customer_sk IS NULL
    """,
    "fct_client_health → dim_date": """
        SELECT COUNT(*) as unmatched FROM `o9-dashboard-493005.dev_marts.fct_client_health` f
        LEFT JOIN `o9-dashboard-493005.dev_marts.dim_date` d ON f.date_sk = d.date_sk
        WHERE d.date_sk IS NULL
    """,
    "fct_client_health → dim_customer": """
        SELECT COUNT(*) as unmatched FROM `o9-dashboard-493005.dev_marts.fct_client_health` f
        LEFT JOIN `o9-dashboard-493005.dev_marts.dim_customer` c ON f.customer_sk = c.customer_sk
        WHERE c.customer_sk IS NULL
    """,
    "fct_advocacy → dim_date": """
        SELECT COUNT(*) as unmatched FROM `o9-dashboard-493005.dev_marts.fct_advocacy` f
        LEFT JOIN `o9-dashboard-493005.dev_marts.dim_date` d ON f.date_sk = d.date_sk
        WHERE d.date_sk IS NULL
    """,
    "fct_advocacy → dim_customer": """
        SELECT COUNT(*) as unmatched FROM `o9-dashboard-493005.dev_marts.fct_advocacy` f
        LEFT JOIN `o9-dashboard-493005.dev_marts.dim_customer` c ON f.customer_sk = c.customer_sk
        WHERE c.customer_sk IS NULL
    """,
    "fct_go_lives → dim_date": """
        SELECT COUNT(*) as unmatched FROM `o9-dashboard-493005.dev_marts.fct_go_lives` f
        LEFT JOIN `o9-dashboard-493005.dev_marts.dim_date` d ON f.date_sk = d.date_sk
        WHERE d.date_sk IS NULL
    """,
    "fct_go_lives → dim_customer": """
        SELECT COUNT(*) as unmatched FROM `o9-dashboard-493005.dev_marts.fct_go_lives` f
        LEFT JOIN `o9-dashboard-493005.dev_marts.dim_customer` c ON f.customer_sk = c.customer_sk
        WHERE c.customer_sk IS NULL
    """,
}

for check, sql in checks.items():
    result = client.query(sql, location="asia-southeast3").result()
    for row in result:
        status = "✓ OK" if row.unmatched == 0 else f"✗ {row.unmatched} UNMATCHED"
        print(f"{check}: {status}")