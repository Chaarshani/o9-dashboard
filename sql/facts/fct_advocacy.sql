CREATE OR REPLACE TABLE `o9-dashboard-493005.dev_marts.fct_advocacy` AS

SELECT
  a.customer_sk,
  a.date_sk,
  c.customer_name,
  c.portfolio,
  c.parent_name,
  a.calendar_month,
  a.period_month,
  a.client_manager,
  a.referenceability,
  a.is_referenceable,
  a.last_review_date,
  a.reason,
  a.stg_loaded_at

FROM `o9-dashboard-493005.dev_staging.stg_advocacy` a
LEFT JOIN `o9-dashboard-493005.dev_staging.stg_customer` c
  ON a.customer_sk = c.customer_sk;