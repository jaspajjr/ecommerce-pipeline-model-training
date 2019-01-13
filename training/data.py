import pandas as pd


def get_query(start_date: str, end_date: str) -> str:
    return '''
    SELECT
     fullVisitorId
     , visitId
     , MIN(visitStartTime) visitStartTime
     , SUM(hits.item.itemRevenue) session_total_revenue
     , MAX(geoNetwork.country) country
     , MAX(trafficSource.medium) medium
     , MAX(device.isMobile) is_mobile
     , COUNT(DISTINCT(p.productSKU)) unique_products_viewed
     , COUNT(DISTINCT(hits.item.productSku)) unique_products_bought
     , MAX(totals.transactionRevenue) lifetime_total_revenue
    FROM `bigquery-public-data.google_analytics_sample.ga_sessions_*`,
        UNNEST(hits) as hits, UNNEST(hits.product) AS p
    WHERE _TABLE_SUFFIX BETWEEN '{start_date}' AND '{end_date}'
    GROUP BY fullVisitorId , visitId
    LIMIT 100
    '''.format(start_date=start_date, end_date=end_date)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['visitStartTime'] = pd.to_datetime(df['visitStartTime'], unit='s')
    df['medium'] = df['medium'].replace('(none)', 'direct')
    df['session_total_revenue'] = df['session_total_revenue'].fillna(0)
    df['lifetime_total_revenue'] = (df['lifetime_total_revenue'] / 1000000.0) \
        .fillna(0)
    return df
