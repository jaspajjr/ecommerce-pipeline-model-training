import json
import pandas as pd


def load_private_key() -> dict:
    with open('/secrets/private-key.json') as f:
        key = json.load(f)

    return key


def get_query() -> str:
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
    WHERE _TABLE_SUFFIX BETWEEN '20160801' AND '20170830'
    GROUP BY fullVisitorId , visitId
    '''


def load_data(query: str, project_id: str, private_key: dict) -> pd.DataFrame:
    return pd.read_gbq(
        query=query,
        project_id=private_key['project_id'],
        private_key=json.dumps(private_key),
        dialect='standard')


def main():
    query = get_query()
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
