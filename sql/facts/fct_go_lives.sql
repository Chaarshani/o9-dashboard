CREATE OR REPLACE TABLE `o9-dashboard-493005.dev_marts.fct_go_lives` AS

SELECT
  g.project_sk,
  g.customer_sk,
  g.date_sk,
  c.customer_name,
  c.portfolio,
  g.customer_region,
  g.project,
  g.project_type,
  g.release,
  g.solution,
  g.client_manager,
  g.release_type,
  g.current_phase,

  -- Dates
  g.blueprint_start,
  g.first_start_date_original,
  g.go_live_original,
  g.blueprint_start_actual,
  g.first_start_date_actual,
  g.actual_go_live,

  -- Duration
  g.duration_original,
  g.duration_actual,
  g.duration_variance,
  CASE
    WHEN g.duration_variance > 0  THEN 'Delayed'
    WHEN g.duration_variance < 0  THEN 'Early'
    WHEN g.duration_variance = 0  THEN 'On Time'
    ELSE 'Unknown'
  END                                                   AS delivery_status,

  -- Delays & TTV
  g.delays,
  g.ttv,
  g.reason_for_delays,

  -- Flags
  g.include_go_live_flag,
  g.pmd_ops_verification_flag,
  g.pmd_ops_comments,

  g.stg_loaded_at

FROM `o9-dashboard-493005.dev_staging.stg_go_lives` g
LEFT JOIN `o9-dashboard-493005.dev_staging.stg_customer` c
  ON g.customer_sk = c.customer_sk;