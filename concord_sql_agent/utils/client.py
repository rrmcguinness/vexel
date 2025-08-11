from google.cloud import bigquery

class ConcordClient():
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConcordClient, cls).__new__(cls)
            cls._instance.client = bigquery.Client(project='concord-prod')
        return cls._instance
