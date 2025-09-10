from google.cloud import bigquery
import google.auth.transport.requests
import google.oauth2.id_token
import google.oauth2.credentials

def get_credentials():
    id_token = None
    try:
        credentials, project_id = google.auth.default()


        target_audience = "https://vexel-service-662234851257.us-central1.run.app" # Replace with your IAP client ID
        auth_req = google.auth.transport.requests.Request()
        id_token = google.oauth2.id_token.fetch_id_token(auth_req, target_audience)

        if id_token:
            credentials.refresh(auth_req)
            access_token = credentials.token
            creds = google.oauth2.credentials.Credentials(token=id_token, refresh_token=access_token)
            return creds
        else:
            return None
    except Exception as e: print(e)

    return None

def get_bq_client() -> bigquery.Client:
    # credentials = get_credentials()
    # if credentials:
    #     return bigquery.Client(project='concord-prod', credentials=credentials)
    # else:
    return bigquery.Client(project='concord-prod')