CREATE OR REPLACE VIEW `o9-dashboard-493005.dev_staging.stg_finance` AS
WITH deduped AS (
  SELECT *,
    ROW_NUMBER() OVER (PARTITION BY customer_customer, month, year ORDER BY customer_customer DESC) AS rn
  FROM `o9-dashboard-493005.dev_raw.raw_finance`
  WHERE customer_customer IS NOT NULL AND TRIM(customer_customer) != ''
)
SELECT
  TO_HEX(MD5(TRIM(customer_customer)))                                 AS customer_sk,
  CAST(CONCAT(CAST(year AS STRING), LPAD(CAST(month AS STRING), 2, '0'), '01') AS INT64) AS date_sk,
  CAST(CONCAT(CAST(year AS STRING), '-', LPAD(CAST(month AS STRING), 2, '0'), '-01') AS DATE) AS period_month,
  NULLIF(TRIM(finance_customer), '')                                   AS finance_customer,
  NULLIF(TRIM(client_manager), '')                                     AS client_manager,
  NULLIF(TRIM(portfolio), '')                                          AS portfolio,
  NULLIF(TRIM(subportfolio), '')                                       AS sub_portfolio,
  month                                                                 AS month_num,
  year                                                                  AS year,
  CAST(services_revenue AS FLOAT64)                                    AS services_revenue,
  CAST(saas_revenue AS FLOAT64)                                        AS saas_revenue,
  CAST(total_revenue AS FLOAT64)                                       AS total_revenue,
  CAST(fac_internal_costs AS FLOAT64)                                  AS fac_internal_costs,
  CAST(fac_external_costs AS FLOAT64)                                  AS fac_external_costs,
  CAST(total_fac_cost AS FLOAT64)                                      AS total_fac_cost,
  CAST(eac_internal_costs AS FLOAT64)                                  AS eac_internal_costs,
  CAST(eac_external_costs AS FLOAT64)                                  AS eac_external_costs,
  CAST(total_eac_cost AS FLOAT64)                                      AS total_eac_cost,
  CAST(services_fac AS FLOAT64)                                        AS services_fac,
  CAST(services_eac AS FLOAT64)                                        AS services_eac,
  CAST(devops_cost AS FLOAT64)                                         AS devops_cost,
  CAST(cs_fac AS FLOAT64)                                              AS cs_fac,
  CAST(cs_eac AS FLOAT64)                                              AS cs_eac,
  CAST(hosting_cost_fac AS FLOAT64)                                    AS hosting_cost_fac,
  CAST(hosting_cost_eac AS FLOAT64)                                    AS hosting_cost_eac,
  CAST(saas_fac AS FLOAT64)                                            AS saas_fac,
  CAST(saas_eac AS FLOAT64)                                            AS saas_eac,
  CURRENT_TIMESTAMP()                                                   AS stg_loaded_at
FROM deduped WHERE rn = 1;