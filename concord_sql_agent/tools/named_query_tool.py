from .named_queries import (qry_forecast, qry_average_daily_run_rate, qry_monthly_actual, qry_committed_workloads)

def create_query_average_daily_run_rate(account_name: str) -> str:
    """
    Gets the BigQuery SQL for calculting the average daily run rate from concord for a sales account.
    Args:
        account_name: str - The name of the account to get the daily run rate for.
    Returns:
        The BigQuery SQL Query to execute.
    """
    return qry_average_daily_run_rate.format(account_name=account_name)


def create_query_get_monthly_actual(account_name: str) -> str:
    """
    Gets the BigQuery SQL query for calculating actual spends by month for the current year.

    Returns:
        The BigQuery SQL Query to execute.
    """
    return qry_monthly_actual.format(account_name=account_name)


def create_query_committed_workloads_for_the_past_twelve_months() -> str:
    """
    Gets the BigQuery SQL query for calculating the committed workloads for the past twelve months
    for the current year.

    Returns:
        The BigQuery SQL Query to execute.
    """
    return qry_committed_workloads.format(account_name='concord-prod')

def create_query_forecast_by_account_name(account_name: str) -> str:
    """
    Gets the BigQuery SQL query for calculating the forecast for a given account name.
    Args:
        account_name: str - The name of the account to get the forecast for.
    Returns:
        The BigQuery SQL Query to execute.
    """
    return qry_forecast.format(account_name=account_name)