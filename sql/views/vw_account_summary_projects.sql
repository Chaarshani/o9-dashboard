CREATE OR REPLACE VIEW `o9-dashboard-493005.dev_marts.vw_account_summary_projects` AS

SELECT
  -- Customer details
  c.customer_sk,
  c.customer_name,
  c.parent_name,
  c.portfolio,
  c.client_manager,
  c.customer_status,

  -- Project details
  g.project_sk,
  g.project,
  g.project_type,
  g.customer_region,
  g.release,
  g.solution,
  g.release_type,
  g.current_phase,

  -- Dates
  g.blueprint_start,
  g.first_start_date_original,
  g.go_live_original,
  g.actual_go_live,

  -- Duration
  g.duration_original,
  g.duration_actual,
  g.duration_variance,
  g.delivery_status,

  -- Delays
  g.delays,
  g.ttv,
  g.reason_for_delays,

  -- Flags
  g.include_go_live_flag,
  g.pmd_ops_verification_flag,
  g.pmd_ops_comments

FROM `o9-dashboard-493005.dev_marts.dim_customer` c
LEFT JOIN `o9-dashboard-493005.dev_marts.fct_go_lives` g
  ON c.customer_sk = g.customer_sk

WHERE c.customer_sk IS NOT NULL;