

import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from typing import Optional
from tools.types import SalesTrajectoryResponse, Chart, StatusMessage


def create_chart_tool(sales_trajectory: str, chart_type: str = "bar", x_axis: str = 'revenue_usage_week', y_axis: str = 'revenue_revenue_sales', title: str = "Sales Trajectory", group_by: Optional[str] = None) -> Chart:
    """
    Generates a chart from a SalesTrajectorResponse and returns its image as a base64 string.

    Args:
        sales_trajectory (str): The response from sales trajectory calls.
        chart_type (str, optional): The type of chart (e.g., "bar", "line", "scatter"). Defaults to "bar".
        x_axis (str, optional): The column for the x-axis. Defaults to 'revenue_usage_week'.
        y_axis (str, optional): The column for the y-axis. Defaults to 'revenue_revenue_sales'.
        title (str, optional): The chart title. Defaults to "Sales Trajectory".
        group_by (str, optional): The column to group by for multi-series charts. Defaults to None.

    Returns:
        dict: A dictionary containing the chart image as a base64 string and a description.
    """
    try:
        # Create the chart using Matplotlib
        plt.figure(figsize=(10, 6))

        tj = SalesTrajectoryResponse.model_validate_json(sales_trajectory)

        if tj and tj.data and tj.status == "success":
            # Use a list comprehension to call .model_dump() on each Pydantic object
            list_of_dicts = [entry.model_dump() for entry in tj.data]
            # Create the DataFrame from the list of dictionaries
            df = pd.DataFrame(list_of_dicts)
            
            # Convert date column and sort values for prettier line charts
            if x_axis in df.columns:
                df[x_axis] = pd.to_datetime(df[x_axis])
                df = df.sort_values(by=x_axis)

            if group_by and group_by in df.columns:
                if chart_type not in ['line', 'scatter']:
                    raise ValueError(f"Grouping is only supported for 'line' and 'scatter' charts, not '{chart_type}'.")
                
                for name, group in df.groupby(group_by):
                    if chart_type == "line":
                        plt.plot(group[x_axis], group[y_axis], label=name)
                    elif chart_type == "scatter":
                        plt.scatter(group[x_axis], group[y_axis], label=name)
                plt.legend()
            else:
                if chart_type == "bar":
                    plt.bar(df[x_axis], df[y_axis])
                elif chart_type == "line":
                    plt.plot(df[x_axis], df[y_axis])
                elif chart_type == "scatter":
                    plt.scatter(df[x_axis], df[y_axis])
                else:
                    raise ValueError(f"Unsupported chart type: {chart_type}")

        plt.xlabel(x_axis)
        plt.ylabel(y_axis)
        plt.title(title)
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Save the chart to a bytes buffer
        buf = BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode("utf-8")
        plt.close()
        
        chart_description = f"A {chart_type} chart titled '{title}' showing {y_axis} against {x_axis}'."
        if group_by:
            chart_description += f" Grouped by {group_by}."

        return Chart(
            status=StatusMessage(status="success", message=f"Chart generated successfully."),
            chart_image=img_base64,
            chart_description=chart_description
        )
    except Exception as e:
        return Chart(
            status=StatusMessage(status="error", message=f"Error generating chart: {str(e)}"),
            chart_image=None,
            chart_description=None
        )


def create_bar_chart(sales_trajectory: str) -> Chart:
    """
    Generates a bar chart from a Sales Trajectory and returns its image as a base64 string.

    Args:
        sales_trajectory (SalesTrajectoryResponse): The response from sales trajectory calls.
        x_axis (str, optional): The column to use for the x-axis. Defaults to None.
        y_axis (str, optional): The column to use for the y-axis. Defaults to None.
        title (str, optional): The chart title. Defaults to "Chart Title".

    Returns:
        dict: A dictionary containing the chart image as a base64 string and a description.
    """
    return create_chart_tool(sales_trajectory=sales_trajectory,
                             chart_type="bar",
                             x_axis='revenue_usage_week',
                             y_axis='revenue_revenue_sales',
                             title='Sales Trajectory',
                             group_by= "products_product")


def create_line_chart(sales_trajectory: str) -> Chart:
    """
    Generates a line chart from a Sales Trajectory JSON representation and returns its image as a base64 string.

    Args:
        sales_trajectory (str): The response from sales trajectory calls.

    Returns:
        dict: A dictionary containing the chart image as a base64 string and a description.
    """
    title = "Sales Trajectory by Product"
    return create_chart_tool(
        sales_trajectory, 
        "line", 
        'revenue_usage_week', 
        'revenue_revenue_sales',
        title=title,
        group_by= "products_product"
    )


def create_scatter_chart(sales_trajectory: str) -> Chart:
    """
    Generates a scatter chart from a Sales Trajectory and returns its image as a base64 string.

    Args:
        sales_trajectory (str): The json representation of s sale trajectory

    Returns:
        dict: A dictionary containing the chart image as a base64 string and a description.
    """
    return create_chart_tool(sales_trajectory, "scatter", 'revenue_usage_week', 'revenue_revenue_sales', "Sales Trajectory",  group_by= "products_product")

