"""
Thq queries in this file were all created by the Query Tool
"""

qry_average_daily_run_rate = """
WITH YTD_Totals AS (
    SELECT customer_details.account_name, SUM(usd_revenue_metrics.sales_revenue.sales_revenue) AS total_revenue_ytd
    FROM `concord-prod.service_cloudbi_reporting.revenue_weekly`
    WHERE partition_date BETWEEN DATE_TRUNC(CURRENT_DATE(), YEAR) AND CURRENT_DATE() AND customer_details.account_name = '{account_name}'
    GROUP BY customer_details.account_name)
SELECT account_name, total_revenue_ytd, DATE_DIFF(CURRENT_DATE(), DATE_TRUNC(CURRENT_DATE(), YEAR), DAY) + 1 AS days_in_ytd_period, SAFE_DIVIDE(total_revenue_ytd, DATE_DIFF(CURRENT_DATE(), DATE_TRUNC(CURRENT_DATE(), YEAR), DAY) + 1) AS daily_run_rate_ytd
FROM
    YTD_Totals;"""

qry_monthly_actual = """
SELECT
   invoice_month_start AS revenue_month, SUM(usd_revenue_metrics.sales_revenue.sales_revenue) AS total_sales_revenue
FROM `concord-prod.service_cloudbi_reporting.revenue_weekly`
WHERE partition_date BETWEEN DATE_TRUNC(CURRENT_DATE(), YEAR) AND CURRENT_DATE()
GROUP BY revenue_month
ORDER BY revenue_month ASC;"""

qry_committed_workloads = """
WITH
    MonthlyUsageByProduct AS (
        SELECT
            invoice_month_start AS revenue_month, product_details.gtm_product_hierarchy.gtm_product_level_3 AS gtm_product_category, SUM(usd_revenue_metrics.gross_revenue.gross_revenue) AS total_gross_revenue
        FROM `concord-prod.service_cloudbi_reporting.revenue_weekly`
        WHERE partition_date BETWEEN DATE_TRUNC(CURRENT_DATE(), YEAR) AND CURRENT_DATE() AND customer_details.account_name = '{account_name}'
        GROUP BY 1, 2),

    MonthlyCommitmentRevenue AS (
        SELECT invoice_month_start AS revenue_month,
               SUM(IFNULL(usd_revenue_metrics.invoice_revenue.components.sales_discounts.cud, 0) + IFNULL(usd_revenue_metrics.invoice_revenue.components.sales_discounts.spend_based_commitment_discount, 0)) AS total_committed_revenue
        FROM `concord-prod.service_cloudbi_reporting.revenue_weekly`
        WHERE partition_date BETWEEN DATE_TRUNC(CURRENT_DATE(), YEAR) AND CURRENT_DATE() AND customer_details.account_name = '{account_name}'
          AND (usd_revenue_metrics.invoice_revenue.components.sales_discounts.cud IS NOT NULL OR usd_revenue_metrics.invoice_revenue.components.sales_discounts.spend_based_commitment_discount IS NOT NULL)
        GROUP BY 1
    )

SELECT usage.revenue_month, usage.gtm_product_category, usage.total_gross_revenue,
       SUM(usage.total_gross_revenue) OVER (PARTITION BY usage.revenue_month) AS total_monthly_gross_revenue,
    SAFE_DIVIDE(usage.total_gross_revenue, SUM(usage.total_gross_revenue) OVER (PARTITION BY usage.revenue_month)) * commitments.total_committed_revenue AS allocated_committed_revenue
FROM MonthlyUsageByProduct AS usage
JOIN
MonthlyCommitmentRevenue AS commitments
ON usage.revenue_month = commitments.revenue_month
WHERE
    usage.gtm_product_category IS NOT NULL
ORDER BY
    usage.revenue_month ASC,
    allocated_committed_revenue DESC;"""

qry_forecast = """
WITH
    DailyRunRate AS (
        SELECT
            SAFE_DIVIDE(SUM(usd_revenue_metrics.sales_revenue.sales_revenue), DATE_DIFF(CURRENT_DATE(), DATE_TRUNC(CURRENT_DATE(), YEAR), DAY) + 1) AS drr
        FROM `concord-prod.service_cloudbi_reporting.revenue_weekly`
        WHERE
            partition_date BETWEEN DATE_TRUNC(CURRENT_DATE(), YEAR) AND CURRENT_DATE() AND customer_details.account_name = '{account_name}'
          AND customer_details.account_name = '{account_name}'),

    MonthlyActuals AS (
        SELECT invoice_month_start AS revenue_month, SUM(usd_revenue_metrics.sales_revenue.sales_revenue) AS total_actuals
        FROM `concord-prod.service_cloudbi_reporting.revenue_weekly`
        WHERE
            partition_date BETWEEN DATE_TRUNC(CURRENT_DATE(), YEAR) AND CURRENT_DATE() AND customer_details.account_name = '{account_name}'
          AND customer_details.account_name = '{account_name}'
        GROUP BY 1),

    MonthlyCommittedWorkloads AS (
        SELECT
            revenue_month,
            SUM(allocated_committed_revenue) AS total_committed
        FROM (
                 WITH MonthlyUsageByProduct AS (
                     SELECT invoice_month_start AS revenue_month, product_details.gtm_product_hierarchy.gtm_product_level_3 AS gtm_product_category, SUM(usd_revenue_metrics.gross_revenue.gross_revenue) AS total_gross_revenue
                     FROM `concord-prod.service_cloudbi_reporting.revenue_weekly`
                     WHERE partition_date BETWEEN DATE_TRUNC(CURRENT_DATE(), YEAR) AND CURRENT_DATE() AND customer_details.account_name = '{account_name}' GROUP BY 1, 2),

                      MonthlyCommitmentRevenue AS (
                          SELECT invoice_month_start AS revenue_month, SUM(IFNULL(usd_revenue_metrics.invoice_revenue.components.sales_discounts.cud, 0) + IFNULL(usd_revenue_metrics.invoice_revenue.components.sales_discounts.spend_based_commitment_discount, 0)) AS total_committed_revenue
                          FROM `concord-prod.service_cloudbi_reporting.revenue_weekly`
                          WHERE partition_date BETWEEN DATE_TRUNC(CURRENT_DATE(), YEAR) AND CURRENT_DATE() AND customer_details.account_name = '{account_name}'
                          GROUP BY 1)

                 SELECT  usage.revenue_month, SAFE_DIVIDE(usage.total_gross_revenue, SUM(usage.total_gross_revenue) OVER (PARTITION BY usage.revenue_month)) * commitments.total_committed_revenue AS allocated_committed_revenue
                 FROM MonthlyUsageByProduct AS usage JOIN MonthlyCommitmentRevenue AS commitments ON usage.revenue_month = commitments.revenue_month
                 WHERE usage.gtm_product_category IS NOT NULL)
        GROUP BY 1),

    AllMonthsInYear AS (SELECT month_start FROM UNNEST(GENERATE_DATE_ARRAY(DATE_TRUNC(CURRENT_DATE(), YEAR), DATE_ADD(DATE_TRUNC(CURRENT_DATE(), YEAR), INTERVAL 11 MONTH), INTERVAL 1 MONTH)) AS month_start),

    CombinedData AS (
        SELECT
            cal.month_start,
            IFNULL(act.total_actuals, 0) AS monthly_actuals,
            IFNULL(com.total_committed, 0) AS monthly_committed,
            drr.drr

        FROM AllMonthsInYear AS cal
                 LEFT JOIN MonthlyActuals AS act ON cal.month_start = act.revenue_month
                 LEFT JOIN MonthlyCommittedWorkloads AS com ON cal.month_start = com.revenue_month
                 CROSS JOIN DailyRunRate AS drr),

    ForecastLogic AS (
        SELECT month_start,
               CASE
                   WHEN month_start < DATE_TRUNC(CURRENT_DATE(), MONTH) THEN monthly_actuals
                   WHEN month_start = DATE_TRUNC(CURRENT_DATE(), MONTH) THEN monthly_actuals + (drr * GREATEST(0, DATE_DIFF(LAST_DAY(month_start), CURRENT_DATE(), DAY))) + monthly_committed
                   ELSE (drr * (DATE_DIFF(LAST_DAY(month_start), month_start, DAY) + 1)) + monthly_committed END AS forecast_value
        FROM CombinedData),
    PivotedForecast AS (
        SELECT *
        FROM (SELECT FORMAT_DATE('%B', month_start) AS month_name, forecast_value
              FROM ForecastLogic)

                 PIVOT (SUM(forecast_value) FOR month_name IN ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')))
SELECT *, (January + February + March + April + May + June + July + August + September + October + November + December) AS Flat_Total, 10000 AS BCFM_Magic
FROM PivotedForecast;"""



