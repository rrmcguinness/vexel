import pandas as pd
from google.api_core.exceptions import GoogleAPIError

from ..utils.client import get_bq_client

# Set the global float format for MD output
pd.options.display.float_format = '{:,.2f}'.format

timeout_seconds = 120

def execute_query(query: str) -> str:
    """Executes a Concord Query in BigQuery and returns the results in markdown format.

    Args:
        query: Ths BigQuery SQL statement to execute.

    Returns:
        A markdown formatted table of the data requested.
    """
    try:
        client = get_bq_client()
        query_job = client.query(query, timeout=timeout_seconds)
        rows = query_job.result()
        df = rows.to_dataframe()
        return df.to_markdown(index=False, floatfmt=",.2f")
    except GoogleAPIError as e:  # Catch the timeout exception
        print(f"Query timed out after {timeout_seconds} seconds with the following error: {e}\nOptimize this query and try again.")
    except Exception as e:
        print(e)
        return f"The following Error occurred:\n{e}\nFix the error and retry."
