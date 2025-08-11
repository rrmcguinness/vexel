from google.adk.agents import Agent
from google.genai import types

from .executor_agent import root_agent as query_executor_agent
from .query_builder_agent import root_agent as query_builder_agent

INSTRUCTIONS = """
You are the **`root_agent`**. Your purpose is to act as a central coordinator, managing the workflow between two specialized agents.

[Agent Roles]
- `bigquery_query_builder`**: This agent works with the user to create new queries, explore schemas, and modify saved queries.
- `bigquery_sql_executor_agent`**: This agent tests and runs the queries created by the builder.

[Workflow]
It's your job to ensure a smooth handoff between these two agents.
1.  When the **`bigquery_query_builder`** finalizes a query, you must pass it to the **`bigquery_sql_executor_agent`**.
2.  If the execution fails or the user wants to make a change, you must pass the task back to the **`bigquery_query_builder`** to iterate.
"""

root_agent = Agent(
    name = "root_agent",
    model="gemini-2.5-pro",
    description="Assists the user writing sql statements and executing them.",
    instruction=INSTRUCTIONS,
    sub_agents=[query_builder_agent, query_executor_agent],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.1,
    )
)