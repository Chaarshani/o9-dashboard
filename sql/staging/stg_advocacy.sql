CREATE OR REPLACE VIEW `o9-dashboard-493005.dev_staging.stg_advocacy` AS
WITH deduped AS (
  SELECT *,
    ROW_NUMBER() OVER (PARTITION BY customer, time__calendar_month_ ORDER BY customer DESC) AS rn
  FROM `o9-dashboard-493005.dev_raw.raw_advocacy`
  WHERE customer IS NOT NULL AND TRIM(customer) != ''
)
SELECT
  TO_HEX(MD5(TRIM(customer)))                                          AS customer_sk,
  NULLIF(TRIM(customer_portfolio), '')                                 AS portfolio,
  NULLIF(TRIM(client_manager), '')                                     AS client_manager,
  NULLIF(TRIM(time__calendar_month_), '')                              AS calendar_month,
  SAFE.PARSE_DATE('%B %Y', time__calendar_month_)                      AS period_month,
  CAST(FORMAT_DATE('%Y%m%d',
    COALESCE(SAFE.PARSE_DATE('%B %Y', time__calendar_month_),
             CURRENT_DATE())) AS INT64)                                AS date_sk,
  SAFE.PARSE_DATE('%m/%d/%Y', last_reviewed_date)                      AS last_review_date,
  NULLIF(TRIM(referenceability), '')                                   AS referenceability,
  CASE
    WHEN UPPER(TRIM(referenceability)) IN ('YES','Y','TRUE')  THEN TRUE
    WHEN UPPER(TRIM(referenceability)) IN ('NO','N','FALSE')  THEN FALSE
    ELSE NULL
  END                                                                   AS is_referenceable,
  NULLIF(TRIM(reason_for_non_referenceability), '')                    AS reason,
  CURRENT_TIMESTAMP()                                                   AS stg_loaded_at
FROM deduped WHERE rn = 1;