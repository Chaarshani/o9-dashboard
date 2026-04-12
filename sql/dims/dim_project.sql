CREATE OR REPLACE TABLE `o9-dashboard-493005.dev_marts.dim_project` AS

SELECT
  p.project_sk,
  p.customer_sk,
  c.customer_name,
  c.portfolio                                           AS customer_portfolio,
  p.project,
  p.country,
  p.region,
  p.portfolio                                           AS project_portfolio,
  p.sub_portfolio,
  p.portfolio_leader,
  p.client_manager,
  p.project_type,
  p.project_sow_status,
  p.contract_type,
  p.project_start_date,
  p.project_end_date,
  DATE_DIFF(
    COALESCE(p.project_end_date, CURRENT_DATE()),
    p.project_start_date,
    MONTH
  )                                                     AS project_duration_months,
  CASE
    WHEN p.project_end_date IS NULL                     THEN 'Active'
    WHEN p.project_end_date >= CURRENT_DATE()           THEN 'Active'
    ELSE 'Completed'
  END                                                   AS project_status,
  p.requested_count,
  p.allocated_count,
  p.unallocated_count,
  p.requested_lifetime_count,
  p.stg_loaded_at

FROM `o9-dashboard-493005.dev_staging.stg_project` p
LEFT JOIN `o9-dashboard-493005.dev_staging.stg_customer` c
  ON p.customer_sk = c.customer_sk

WHERE p.project_sk IS NOT NULL;