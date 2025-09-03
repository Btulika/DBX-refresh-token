# refresh_pgpassword.py
import requests
from databricks.sdk import WorkspaceClient
from databricks.sdk.core import Config

# Load Databricks config (uses env vars / cluster context)
cfg = Config()
w = WorkspaceClient(config=cfg)

CLIENT_ID = cfg.client_id
CLIENT_SECRET = cfg.client_secret
HOST = cfg.host.rstrip('/')

# 1. Request new token from Databricks OAuth endpoint
resp = requests.post(
    f"{HOST}/oidc/v1/token",
    auth=(CLIENT_ID, CLIENT_SECRET),
    headers={"Content-Type": "application/x-www-form-urlencoded"},
    data={"grant_type": "client_credentials", "scope": "all-apis"}
)
resp.raise_for_status()
token = resp.json()["access_token"]

# 2. Store into secret scope
w.secrets.put_secret(scope="my-oauth-secrets", key="pgpassword", string_value=token)

print("✅ Refreshed pgpassword and stored in Databricks Secrets")
