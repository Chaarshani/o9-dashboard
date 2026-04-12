CREATE OR REPLACE VIEW `o9-dashboard-493005.dev_staging.stg_go_lives` AS
WITH deduped AS (
  SELECT *,
    ROW_NUMBER() OVER (PARTITION BY project, customer ORDER BY project DESC) AS rn
  FROM `o9-dashboard-493005.dev_raw.raw_go_lives`
  WHERE project IS NOT NULL AND TRIM(project) != ''
)
SELECT
  TO_HEX(MD5(TRIM(project)))                                           AS project_sk,
  TO_HEX(MD5(TRIM(customer)))                                          AS customer_sk,
  TRIM(customer)                                                         AS customer_name,
  NULLIF(TRIM(customer_region), '')                                    AS customer_region,
  TRIM(project)                                                          AS project,
  NULLIF(TRIM(project_type), '')                                       AS project_type,
  NULLIF(TRIM(customer_portfolio), '')                                 AS portfolio,
  NULLIF(TRIM(release), '')                                            AS release,
  NULLIF(TRIM(solution), '')                                           AS solution,
  NULLIF(TRIM(client_manager), '')                                     AS client_manager,
  NULLIF(TRIM(release_type), '')                                       AS release_type,
  NULLIF(TRIM(current_phase), '')                                      AS current_phase,

  -- Dates: format is YYYY-MM-DD, but some values are the string 'None'
  SAFE.PARSE_DATE('%Y-%m-%d', NULLIF(TRIM(blueprint_start), 'None'))            AS blueprint_start,
  SAFE.PARSE_DATE('%Y-%m-%d', NULLIF(TRIM(first_start_date_original), 'None'))  AS first_start_date_original,
  SAFE.PARSE_DATE('%Y-%m-%d', NULLIF(TRIM(go_live), 'None'))                    AS go_live_original,
  SAFE.PARSE_DATE('%Y-%m-%d', NULLIF(TRIM(blueprint_start_actual), 'None'))     AS blueprint_start_actual,
  SAFE.PARSE_DATE('%Y-%m-%d', NULLIF(TRIM(first_start_date_actual), 'None'))    AS first_start_date_actual,
  SAFE.PARSE_DATE('%Y-%m-%d', NULLIF(TRIM(actual_golive), 'None'))              AS actual_go_live,

  duration_o                                                             AS duration_original,
  CAST(NULLIF(TRIM(CAST(duration AS STRING)), 'None') AS FLOAT64)       AS duration_actual,
  CAST(duration AS FLOAT64) - CAST(duration_o AS FLOAT64)               AS duration_variance,
  delays_for_project_release                                             AS delays,
  ttv_for_project_release                                                AS ttv,
  NULLIF(TRIM(reason_for_delays__high_ttv), '')                         AS reason_for_delays,

  -- date_sk: use actual_golive first, fall back to go_live
  CAST(FORMAT_DATE('%Y%m%d',
    COALESCE(
      SAFE.PARSE_DATE('%Y-%m-%d', NULLIF(TRIM(actual_golive), 'None')),
      SAFE.PARSE_DATE('%Y-%m-%d', NULLIF(TRIM(go_live), 'None'))
    )) AS INT64)                                                         AS date_sk,

  CASE
    WHEN UPPER(TRIM(include_go_live_flag)) IN ('TRUE','YES','1','Y')    THEN TRUE
    WHEN UPPER(TRIM(include_go_live_flag)) IN ('FALSE','NO','0','N')    THEN FALSE
    ELSE NULL
  END                                                                    AS include_go_live_flag,
  NULLIF(TRIM(pmd_ops_verification_flag), '')                           AS pmd_ops_verification_flag,
  NULLIF(TRIM(pmd_ops_comments), '')                                    AS pmd_ops_comments,
  CURRENT_TIMESTAMP()                                                    AS stg_loaded_at

FROM deduped WHERE rn = 1;