CREATE OR REPLACE TABLE `o9-dashboard-493005.dev_marts.fct_client_health` AS

SELECT
  h.customer_sk,
  h.date_sk,
  c.customer_name,
  c.portfolio,
  c.parent_name,
  h.calendar_month,
  h.period_month,
  h.client_manager,
  h.client_health_score,
  h.client_health_std,
  h.notes,
  h.last_review_date,
  h.stg_loaded_at

FROM `o9-dashboard-493005.dev_staging.stg_client_health` h
LEFT JOIN `o9-dashboard-493005.dev_staging.stg_customer` c
  ON h.customer_sk = c.customer_sk;