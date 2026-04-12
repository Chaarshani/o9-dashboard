CREATE OR REPLACE VIEW `o9-dashboard-493005.dev_staging.stg_project` AS
WITH deduped AS (
  SELECT *,
    ROW_NUMBER() OVER (PARTITION BY project, customer ORDER BY project DESC) AS rn
  FROM `o9-dashboard-493005.dev_raw.raw_project`
  WHERE project IS NOT NULL AND TRIM(project) != ''
)
SELECT
  TO_HEX(MD5(TRIM(project)))                                          AS project_sk,
  TO_HEX(MD5(TRIM(customer)))                                         AS customer_sk,
  TRIM(project)                                                         AS project,
  TRIM(customer)                                                        AS customer_name,
  NULLIF(TRIM(country), '')                                            AS country,
  NULLIF(TRIM(region), '')                                             AS region,
  NULLIF(TRIM(customer_portfolio), '')                                 AS portfolio,
  NULLIF(TRIM(customer_sub_portfolio), '')                             AS sub_portfolio,
  NULLIF(TRIM(portfolio_leader), '')                                   AS portfolio_leader,
  NULLIF(TRIM(client_manager), '')                                     AS client_manager,
  NULLIF(TRIM(project_type), '')                                       AS project_type,
  NULLIF(TRIM(project_sow_status), '')                                 AS project_sow_status,
  NULLIF(TRIM(contract_type), '')                                      AS contract_type,
  SAFE.PARSE_DATE('%m/%d/%Y', project_start_date)                      AS project_start_date,
  SAFE.PARSE_DATE('%m/%d/%Y', project_end_date)                        AS project_end_date,
  requested_count_c_f                                                   AS requested_count,
  allocated_count_c_f                                                   AS allocated_count,
  unallocated_count_c_f                                                 AS unallocated_count,
  requested_lifetime_count                                              AS requested_lifetime_count,
  CURRENT_TIMESTAMP()                                                   AS stg_loaded_at
FROM deduped WHERE rn = 1;