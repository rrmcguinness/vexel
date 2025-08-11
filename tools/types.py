from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Any, List, Literal, Optional
from datetime import datetime
from enum import Enum

class StatusMessage(BaseModel):
    status: Literal["success", "error"]
    message: str

class SalesTrajectoryResponse(BaseModel):
    status: StatusMessage
    data: Optional[List["WeeklyRevenue"]]

class Chart(BaseModel):
    status: StatusMessage
    chart_image: str | None
    chart_description: str | None

class ProductEnum(str, Enum):
    """
    Enum to represent the possible product categories.
    Using an Enum provides strong type validation and autocompletion in your IDE.
    """
    DATA_ANALYTICS_CORE = 'Data Analytics (Core)'
    SECURITY = 'Security'
    LOOKER = 'Looker'
    APIGEE = 'Apigee'
    MARKETPLACE = 'Marketplace'
    GCP_SAAS = 'GCP SaaS'
    GCP_CLASSIC = 'GCP Classic'
    DATABASES = 'Databases'
    GCP_AI = 'GCP AI'
    CLOUD_AI = 'Cloud AI'
    INFRA_AI = 'Infra AI'
    GEMINI_AI = 'Gemini AI'
    GEO = 'Geo'
    PSO = 'PSO'
    WORKSPACE = 'Workspace'
    MANDIANT_CONSULTING = 'Mandiant Consulting'

class WeeklyRevenue(BaseModel):
    """
    Represents a single row of the weekly revenue data from the BigQuery query.
    Field names are Pythonic (snake_case) and mapped to BQ columns using aliases.
    """
    # Removed deprecated 'anystr_strip_whitespace=True'
    model_config = ConfigDict(from_attributes=True)

    product: ProductEnum = Field(
        ...,
        alias="products_product",
        description="The human-readable product category name."
    )
    product_sort_key: str = Field(
        ...,
        alias="products_product__sort_",
        description="A key used for sorting the product categories."
    )
    usage_week: datetime.date = Field(
        ...,
        alias="revenue_usage_week",
        description="The Monday of the week for which the revenue is reported."
    )
    sales_revenue: Optional[float] = Field(
        None,
        alias="revenue_revenue_sales",
        description="The calculated sales revenue for the product in that week."
    )

    @field_validator('*', mode='before')
    @classmethod
    def strip_whitespace(cls, v: Any) -> Any:
        """Strips leading/trailing whitespace from all string fields."""
        if isinstance(v, str):
            return v.strip()
        return v

class WorkloadForecastWrapper(BaseModel):
    status: StatusMessage
    data: List[WeeklyRevenue]