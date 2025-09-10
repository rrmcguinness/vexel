import json
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from ..utils.client import get_bq_client


class SchemaMeta(BaseModel):
    display_name: Optional[str]
    full_name: str
    created: datetime
    updated: datetime
    description: str
    schema_json: list = []

def get_bigquery_table_schema(table_ref: str) -> str:
    """Retrieves the schema of a BigQuery table as a dictionary."""
    table = get_bq_client().get_table(table_ref)
    schema_map = [field.to_api_repr() for field in table.schema]
    print(schema_map)
    return SchemaMeta(display_name=table.friendly_name,
                      full_name=table_ref,
                      created=table.created,
                      updated=table.modified,
                      description=table.description,
                      schema_json=schema_map).model_dump_json()

schema_names = [
    "concord-prod.service_cloudbi_reporting.revenue_daily",
    "concord-prod.service_cloudbi_reporting.revenue_project_sku_daily"
]

all_schemas: list[str] = []

for schema_name in schema_names:
    all_schemas.append(get_bigquery_table_schema(schema_name))

schema_json_array = json.dumps(all_schemas)