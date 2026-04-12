CREATE OR REPLACE TABLE `o9-dashboard-493005.dev_marts.fct_financials` AS

SELECT
  f.customer_sk,
  f.date_sk,
  c.customer_name,
  c.portfolio,
  c.client_manager,
  f.period_month,
  f.month_num,
  f.year,
  f.finance_customer,
  f.sub_portfolio,

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
  COALESCE(f.total_revenue, 0) - COALESCE(f.total_fac_cost, 0) AS gross_margin_fac,
  COALESCE(f.total_revenue, 0) - COALESCE(f.total_eac_cost, 0) AS gross_margin_eac,
  CASE
    WHEN COALESCE(f.total_revenue, 0) = 0 THEN NULL
    ELSE ROUND(
      (COALESCE(f.total_revenue, 0) - COALESCE(f.total_fac_cost, 0))
      / f.total_revenue * 100, 2)
  END                                                   AS margin_pct_fac,
  CASE
    WHEN COALESCE(f.total_revenue, 0) = 0 THEN NULL
    ELSE ROUND(
      (COALESCE(f.total_revenue, 0) - COALESCE(f.total_eac_cost, 0))
      / f.total_revenue * 100, 2)
  END                                                   AS margin_pct_eac,

  f.stg_loaded_at

FROM `o9-dashboard-493005.dev_staging.stg_finance` f
LEFT JOIN `o9-dashboard-493005.dev_staging.stg_customer` c
  ON f.customer_sk = c.customer_sk;