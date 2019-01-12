import json
import pandas as pd


def load_private_key() -> dict:
    with open('/secrets/private-key.json') as f:
        key = json.load(f)

    return key


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


def load_data(query: str, project_id: str, private_key: dict) -> pd.DataFrame:
    return pd.read_gbq(
        query=query,
        project_id=private_key['project_id'],
        private_key=json.dumps(private_key),
        dialect='standard')


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['visitStartTime'] = pd.to_datetime(df['visitStartTime'], unit='s')
    df['lifetime_total_revenue'] = (df['lifetime_total_revenue'] / 1000000.0)
    return df


def main():
    query = get_query(start_date='20160801', end_date='20170830')
    print(query)
    private_key = load_private_key()
    print(private_key)
    df = load_data(
        query=query,
        project_id=private_key['project_id'],
        private_key=private_key)

    return df


if __name__ == "__main__":
    print(main())
