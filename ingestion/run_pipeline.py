import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
import gspread
from oauth2client.service_account import ServiceAccountCredentials

PROJECT_ID     = "o9-dashboard-493005"
DATASET_ID     = "dev_raw"
SPREADSHEET_ID = "1gZ2nizF-X18SrAUqnIc6l7GRBPVMO8gbM-oQErKjges"

SHEET_TO_TABLE = {
    "raw_cust":          "raw_customer",
    "raw_project":       "raw_project",
    "raw_advocacy":      "raw_advocacy",
    "raw_client_health": "raw_client_health",
    "raw_go_lives":      "raw_go_lives",
    "raw_finance":       "raw_finance",
}

def get_sheet_data(sheet_name):
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "secrets/service_account.json", scope
    )
    client      = gspread.authorize(creds)
    spreadsheet = client.open_by_key(SPREADSHEET_ID)
    worksheet   = spreadsheet.worksheet(sheet_name)
    data        = worksheet.get_all_records()
    df          = pd.DataFrame(data)

    # Clean column names for BigQuery compatibility
    df.columns = (
        df.columns
        .str.strip()
        .str.replace(r'[.\[\]\s\/]', '_', regex=True)
        .str.replace(r'[^a-zA-Z0-9_]', '', regex=True)
        .str.lower()
    )

    return df

def clean_dataframe(df):
    for col in df.columns:
        # Replace empty strings with None
        df[col] = df[col].replace('', None)

        # Try to convert to numeric, if it fails keep as string
        try:
            converted = pd.to_numeric(df[col], errors='raise')
            df[col] = converted
        except (ValueError, TypeError):
            df[col] = df[col].astype(str).where(df[col].notna(), None)

    return df

def load_to_bq(df, table_name):
    # Clean data before loading
    df = clean_dataframe(df)

    creds = service_account.Credentials.from_service_account_file(
        "secrets/service_account.json",
        scopes=["https://www.googleapis.com/auth/bigquery"]
    )
    client    = bigquery.Client(project=PROJECT_ID, credentials=creds)
    table_id  = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE",
        autodetect=True
    )
    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()
    print(f"  ✓ Loaded {len(df)} rows into {table_id}")

def main():
    for sheet_tab, bq_table in SHEET_TO_TABLE.items():
        print(f"Loading {sheet_tab} → {DATASET_ID}.{bq_table} ...")
        df = get_sheet_data(sheet_tab)
        if df.empty:
            print(f"  ⚠ Skipping — no data found in {sheet_tab}")
            continue
        load_to_bq(df, bq_table)
    print("\n✅ All sheets loaded into BigQuery successfully!")

if __name__ == "__main__":
    main()