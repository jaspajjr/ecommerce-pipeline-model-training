import datetime
import os
import json
import pandas as pd
from google.cloud import storage
from data import get_query, clean_data


def load_configuration() -> dict:
    with open('/secrets/config-details.json') as f:
        config = json.load(f)
    return config


def load_private_key() -> dict:
    with open('/secrets/private-key.json') as f:
        key = json.load(f)

    return key


def store_training_data(df: pd.DataFrame):
    client = storage.Client.from_service_account_json(
        '/secrets/private-key.json')
    bucket_name = load_configuration()['bucketname']
    file_name = 'training_data_{timestamp}.csv'.format(
        timestamp=datetime.datetime.now())
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(os.path.join(bucket_name, file_name))
    blob.upload_from_string(df.to_string())


def load_data(query: str, project_id: str, private_key: dict) -> pd.DataFrame:
    return pd.read_gbq(
        query=query,
        project_id=private_key['project_id'],
        private_key=json.dumps(private_key),
        dialect='standard')


def main():
    query = get_query(start_date='20160801', end_date='20170830')
    print(query)
    private_key = load_private_key()
    df = load_data(
        query=query,
        project_id=private_key['project_id'],
        private_key=private_key)

    store_training_data(clean_data(df))
    return df


if __name__ == "__main__":
    print(main())
