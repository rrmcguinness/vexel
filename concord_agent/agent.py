from google.genai import types
from google.adk.agents import Agent
from tools import concord as concord_tools

INSTRUCTIONS = """[Purpose]
Retrieve data from the concord database and format it into a JSON object for downstream agents.
"""

root_agent = Agent(
    name = "concord_agent",
    model="gemini-2.5-pro",
    description="Provides read access to sales information base on the current user.",
    instruction=INSTRUCTIONS,
    output_key="sales_trajectory",
    tools=[concord_tools.product_sales_trajectory.query,
           concord_tools.commited_monthly_workloads.query],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.1,
    )
)