CREATE OR REPLACE VIEW `o9-dashboard-493005.dev_marts.vw_account_summary_customer` AS

SELECT
  -- Customer details
  c.customer_sk,
  c.customer_name,
  c.parent_name,
  c.portfolio,
  c.client_manager,
  c.customer_status,

  -- Date details
  d.date_sk,
  d.year,
  d.month_num,
  d.month_name,
  d.year_month,
  d.quarter,
  d.half_year,

  -- Client health
  h.client_health_score,
  h.client_health_std,
  h.notes                                               AS health_notes,
  h.last_review_date                                    AS health_last_review_date,

  -- Advocacy
  a.referenceability,
  a.is_referenceable,
  a.reason                                              AS advocacy_reason,
  a.last_review_date                                    AS advocacy_last_review_date,

  -- Revenue
  COALESCE(f.services_revenue, 0)                       AS services_revenue,
  COALESCE(f.saas_revenue, 0)                           AS saas_revenue,
  COALESCE(f.total_revenue, 0)                          AS total_revenue,

  -- FAC costs
  COALESCE(f.fac_internal_costs, 0)                     AS fac_internal_costs,
  COALESCE(f.fac_external_costs, 0)                     AS fac_external_costs,
  COALESCE(f.total_fac_cost, 0)                         AS total_fac_cost,
  COALESCE(f.services_fac, 0)                           AS services_fac,
  COALESCE(f.cs_fac, 0)                                 AS cs_fac,
  COALESCE(f.hosting_cost_fac, 0)                       AS hosting_cost_fac,
  COALESCE(f.saas_fac, 0)                               AS saas_fac,
  COALESCE(f.devops_cost, 0)                            AS devops_cost,

  -- EAC costs
  COALESCE(f.eac_internal_costs, 0)                     AS eac_internal_costs,
  COALESCE(f.eac_external_costs, 0)                     AS eac_external_costs,
  COALESCE(f.total_eac_cost, 0)                         AS total_eac_cost,
  COALESCE(f.services_eac, 0)                           AS services_eac,
  COALESCE(f.cs_eac, 0)                                 AS cs_eac,
  COALESCE(f.hosting_cost_eac, 0)                       AS hosting_cost_eac,
  COALESCE(f.saas_eac, 0)                               AS saas_eac,

  -- Derived margins
  COALESCE(f.gross_margin_fac, 0)                       AS gross_margin_fac,
  COALESCE(f.gross_margin_eac, 0)                       AS gross_margin_eac,
  f.margin_pct_fac,
  f.margin_pct_eac

FROM `o9-dashboard-493005.dev_marts.dim_customer` c

-- Join to date via finance (finance drives the time dimension)
LEFT JOIN `o9-dashboard-493005.dev_marts.fct_financials` f
  ON c.customer_sk = f.customer_sk
LEFT JOIN `o9-dashboard-493005.dev_marts.dim_date` d
  ON f.date_sk = d.date_sk
LEFT JOIN `o9-dashboard-493005.dev_marts.fct_client_health` h
  ON c.customer_sk = h.customer_sk
  AND f.date_sk = h.date_sk
LEFT JOIN `o9-dashboard-493005.dev_marts.fct_advocacy` a
  ON c.customer_sk = a.customer_sk
  AND f.date_sk = a.date_sk

WHERE c.customer_sk IS NOT NULL;