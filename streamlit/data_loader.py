from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
import streamlit as st
import os

PROJECT  = "o9-dashboard-493005"
LOCATION = "asia-southeast3"

@st.cache_resource
def get_client():
    key_path = "secrets/service_account.json"
    if os.path.exists(key_path):
        credentials = service_account.Credentials.from_service_account_file(
            key_path,
            scopes=["https://www.googleapis.com/auth/bigquery"]
        )
        return bigquery.Client(project=PROJECT, credentials=credentials, location=LOCATION)
    return bigquery.Client(project=PROJECT, location=LOCATION)

@st.cache_data(ttl=3600)
def load_account_summary_customer():
    sql = f"""
        SELECT * FROM `{PROJECT}.dev_marts.vw_account_summary_customer`
        ORDER BY customer_name, year, month_num
    """
    return get_client().query(sql).to_dataframe()

@st.cache_data(ttl=3600)
def load_account_summary_projects():
    sql = f"""
        SELECT * FROM `{PROJECT}.dev_marts.vw_account_summary_projects`
        ORDER BY customer_name, actual_go_live DESC
    """
    return get_client().query(sql).to_dataframe()

@st.cache_data(ttl=3600)
def load_home_kpis():
    sql = f"""
        SELECT
            COUNT(DISTINCT c.customer_sk)                          AS total_customers,
            SUM(f.total_revenue)                                   AS total_revenue,
            ROUND(AVG(f.margin_pct_fac), 1)                        AS avg_margin_pct,
            COUNTIF(h.client_health_std = 'Green')                 AS green_count,
            COUNTIF(h.client_health_std = 'Amber')                 AS amber_count,
            COUNTIF(h.client_health_std = 'Red')                   AS red_count,
            COUNTIF(a.is_referenceable = TRUE)                     AS referenceable_count,
            COUNT(DISTINCT g.project_sk)                           AS total_projects,
            COUNTIF(g.delivery_status = 'On Time')                 AS on_time_count,
            COUNTIF(g.delivery_status = 'Delayed')                 AS delayed_count
        FROM `{PROJECT}.dev_marts.dim_customer` c
        LEFT JOIN `{PROJECT}.dev_marts.fct_financials` f
            ON c.customer_sk = f.customer_sk
        LEFT JOIN `{PROJECT}.dev_marts.fct_client_health` h
            ON c.customer_sk = h.customer_sk
        LEFT JOIN `{PROJECT}.dev_marts.fct_advocacy` a
            ON c.customer_sk = a.customer_sk
        LEFT JOIN `{PROJECT}.dev_marts.fct_go_lives` g
            ON c.customer_sk = g.customer_sk
    """
    df = get_client().query(sql).to_dataframe()
    return df.iloc[0] if not df.empty else None