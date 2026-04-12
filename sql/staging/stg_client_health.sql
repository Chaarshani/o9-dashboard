CREATE OR REPLACE VIEW `o9-dashboard-493005.dev_staging.stg_client_health` AS
WITH deduped AS (
  SELECT *,
    ROW_NUMBER() OVER (PARTITION BY customer, time__calendar_month_ ORDER BY customer DESC) AS rn
  FROM `o9-dashboard-493005.dev_raw.raw_client_health`
  WHERE customer IS NOT NULL AND TRIM(customer) != ''
)
SELECT
  TO_HEX(MD5(TRIM(customer)))                                          AS customer_sk,
  NULLIF(TRIM(customer_parent_name), '')                               AS parent_name,
  NULLIF(TRIM(customer_portfolio), '')                                 AS portfolio,
  NULLIF(TRIM(client_manager), '')                                     AS client_manager,
  NULLIF(TRIM(time__calendar_month_), '')                              AS calendar_month,
  SAFE.PARSE_DATE('%B %Y', time__calendar_month_)                      AS period_month,
  CAST(FORMAT_DATE('%Y%m%d',
    COALESCE(SAFE.PARSE_DATE('%B %Y', time__calendar_month_),
             CURRENT_DATE())) AS INT64)                                AS date_sk,
  client_manager_pov                                                    AS client_health_score,
  CASE
    WHEN client_manager_pov >= 4 THEN 'Green'
    WHEN client_manager_pov = 3  THEN 'Amber'
    WHEN client_manager_pov <= 2 THEN 'Red'
    ELSE 'Unknown'
  END                                                                   AS client_health_std,
  NULLIF(TRIM(notes), '')                                              AS notes,
  SAFE.PARSE_DATE('%m/%d/%Y', last_reviewed_on)                        AS last_review_date,
  CURRENT_TIMESTAMP()                                                   AS stg_loaded_at
FROM deduped WHERE rn = 1;