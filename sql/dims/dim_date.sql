CREATE OR REPLACE TABLE `o9-dashboard-493005.dev_marts.dim_date` AS

WITH date_spine AS (
  SELECT date
  FROM UNNEST(
    GENERATE_DATE_ARRAY('2022-01-01', '2028-12-31', INTERVAL 1 DAY)
  ) AS date
)

SELECT
  CAST(FORMAT_DATE('%Y%m%d', date)       AS INT64)    AS date_sk,
  date                                                  AS date,
  EXTRACT(DAYOFWEEK FROM date)                          AS day_of_week,
  FORMAT_DATE('%A', date)                               AS day_name,
  EXTRACT(DAY FROM date)                                AS day_of_month,
  EXTRACT(DAYOFYEAR FROM date)                          AS day_of_year,
  EXTRACT(WEEK FROM date)                               AS week_of_year,
  EXTRACT(MONTH FROM date)                              AS month_num,
  FORMAT_DATE('%B', date)                               AS month_name,
  FORMAT_DATE('%b', date)                               AS month_short,
  EXTRACT(QUARTER FROM date)                            AS quarter_num,
  CONCAT('Q', CAST(EXTRACT(QUARTER FROM date) AS STRING)) AS quarter,
  CASE
    WHEN EXTRACT(MONTH FROM date) <= 6 THEN 'H1'
    ELSE 'H2'
  END                                                   AS half_year,
  EXTRACT(YEAR FROM date)                               AS year,
  FORMAT_DATE('%Y-%m', date)                            AS year_month,
  CONCAT(
    CAST(EXTRACT(YEAR FROM date) AS STRING), '-Q',
    CAST(EXTRACT(QUARTER FROM date) AS STRING)
  )                                                     AS year_quarter,
  DATE_TRUNC(date, MONTH)                               AS first_day_of_month,
  LAST_DAY(date, MONTH)                                 AS last_day_of_month,
  DATE_TRUNC(date, WEEK)                                AS first_day_of_week,
  DATE_TRUNC(date, YEAR)                                AS first_day_of_year,
  date = DATE_TRUNC(CURRENT_DATE(), MONTH)              AS is_first_day_of_month,
  date = LAST_DAY(CURRENT_DATE(), MONTH)                AS is_last_day_of_month,
  FORMAT_DATE('%Y%m', date) = FORMAT_DATE('%Y%m', CURRENT_DATE()) AS is_current_month,
  EXTRACT(YEAR FROM date) = EXTRACT(YEAR FROM CURRENT_DATE())     AS is_current_year,
  date <= CURRENT_DATE()                                AS is_past_or_present

FROM date_spine
ORDER BY date;