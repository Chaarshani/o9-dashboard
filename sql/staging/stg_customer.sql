CREATE OR REPLACE VIEW `o9-dashboard-493005.dev_staging.stg_customer` AS
WITH deduped AS (
  SELECT *,
    ROW_NUMBER() OVER (PARTITION BY customer__customer_ ORDER BY customer__customer_ DESC) AS rn
  FROM `o9-dashboard-493005.dev_raw.raw_customer`
  WHERE customer__customer_ IS NOT NULL AND TRIM(customer__customer_) != ''
)
SELECT
  TO_HEX(MD5(TRIM(customer__customer_)))                              AS customer_sk,
  NULLIF(TRIM(customer__customer_parent_name_), '')                   AS parent_name,
  TO_HEX(MD5(TRIM(COALESCE(customer__customer_parent_name_, customer__customer_)))) AS parent_sk,
  TRIM(customer__customer_)                                            AS customer_name,
  NULLIF(TRIM(customer__status_), '')                                 AS customer_status,
  NULLIF(TRIM(customer_portfolio), '')                                AS portfolio,
  NULLIF(TRIM(client_manager), '')                                    AS client_manager,
  CURRENT_TIMESTAMP()                                                  AS stg_loaded_at
FROM deduped WHERE rn = 1;