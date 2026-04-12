CREATE OR REPLACE TABLE `o9-dashboard-493005.dev_marts.dim_customer` AS

SELECT
  customer_sk,
  parent_sk,
  parent_name,
  customer_name,
  customer_status,
  portfolio,
  client_manager,
  stg_loaded_at

FROM `o9-dashboard-493005.dev_staging.stg_customer`

WHERE customer_sk IS NOT NULL;