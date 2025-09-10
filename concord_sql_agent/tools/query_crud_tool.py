# query_crud_tools.py

import datetime
import json
import os
from typing import Any, Dict, List

from google.adk.tools import ToolContext
from google.cloud import firestore

# --- Firestore Configuration ---
# In a real ADK deployment, the project ID would typically be inferred from the
# environment where the agent is running.
try:
    db = firestore.Client()
except Exception:
    # Fallback for local development if GOOGLE_CLOUD_PROJECT is not set
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    db_name = os.environ.get("GOOGLE_CLOUD_FIRESTORE_DB_NAME")
    query_collection = os.environ.get("GOOGLE_CLOUD_QUERY_COLLECTION")
    if not project_id:
        raise ValueError(
            "GCP Project ID is not set. Please set the GOOGLE_CLOUD_PROJECT "
            "environment variable."
        )

    if not db_name:
        raise ValueError(
            "FireStore DB Name is not set. Please set the GOOGLE_CLOUD_PROJECT",
            "environment variable"
        )

    if not query_collection:
        raise ValueError(
            "Query collection name is not set, Please set the GOOGLE_CLOUD_QUERY_COLLECTION",
            "environment variable"
        )

    db = firestore.Client(project=project_id, database=db_name)



def create_query(query: str, tool_context: ToolContext) -> Dict[str, Any]:
    """
    Creates a new BigQuery SQL query record in the Firestore database.

    Args:
        query: A JSON string representing the query object to be created.
               The object must conform to the required data structure, including
               fields like name, description, query, is_public, etc.
        tool_context: The context provided by the ADK, used for user info.

    Returns:
        A dictionary representing the newly created query record, including its
        auto-generated Firestore ID.
    """
    query_data = json.loads(query)

    # Add server-side timestamps and creator from the context
    query_data["creator"] = tool_context.user_context.user_id
    query_data["created"] = datetime.datetime.now(datetime.timezone.utc)
    query_data["updated"] = datetime.datetime.now(datetime.timezone.utc)

    # Add the document to Firestore, which auto-generates an ID
    doc_ref = db.collection.document()
    query_data["id"] = doc_ref.id  # Add the generated ID to the document data
    doc_ref.set(query_data)

    return query_data


def list_queries(tool_context: ToolContext) -> List[Dict[str, Any]]:
    """
    Lists all queries created by the current user and all public queries.

    Args:
        tool_context: The context provided by the ADK, used for user info.

    Returns:
        A list of dictionaries, where each dictionary is a query record.
    """
    user_id = tool_context.user_context.user_id
    queries_ref = db.collection(query_collection)

    # Create a compound query to fetch documents where the creator is the
    # current user OR the query is public.
    query = queries_ref.where(
        filter=firestore.Or(
            filters=[
                firestore.FieldFilter("creator", "==", user_id),
                firestore.FieldFilter("is_public", "==", True),
            ]
        )
    )

    docs = query.stream()
    return [doc.to_dict() for doc in docs]


def read_query(query_name: str, tool_context: ToolContext) -> Dict[str, Any]:
    """
    Reads a single query record from Firestore by its name.

    Note: This assumes query names are unique for a given user's accessible
    queries. If multiple queries have the same name, it will return the first
    one found.

    Args:
        query_name: The name of the query to retrieve.
        tool_context: The context provided by the ADK.

    Returns:
        A dictionary representing the found query record.

    Raises:
        ValueError: If no query with the given name is found.
    """
    queries_ref = db.collection(query_collection)
    query = queries_ref.where("name", "==", query_name).limit(1)
    docs = list(query.stream())

    if not docs:
        raise ValueError(f"Query with name '{query_name}' not found.")

    return docs[0].to_dict()


def update_query(query: str, tool_context: ToolContext) -> Dict[str, Any]:
    """
    Updates an existing query record in Firestore.

    The agent's system instructions are responsible for enforcing that a user
    can only update their own queries before calling this tool.

    Args:
        query: A JSON string of the query object with updated fields. This
               object MUST include the 'id' of the document to update.
        tool_context: The context provided by the ADK.

    Returns:
        A dictionary representing the fully updated query record.

    Raises:
        ValueError: If the 'id' field is missing from the input query object.
    """
    updated_data = json.loads(query)
    doc_id = updated_data.get("id")

    if not doc_id:
        raise ValueError(
            "The 'id' field is required in the query object for updates."
        )

    query_ref = db.collection(query_collection)

    doc_ref = query_ref.document(doc_id)

    # Ensure the updated timestamp is set to now
    updated_data["updated"] = datetime.datetime.now(datetime.timezone.utc)

    # Use set with merge=True to update fields or create them if they don't exist
    doc_ref.set(updated_data, merge=True)

    # Return the full, updated document
    updated_doc = doc_ref.get()
    return updated_doc.to_dict()


def delete_query(query_name: str, tool_context: ToolContext) -> bool:
    """
    Deletes a query record from Firestore by its name.

    The agent's system instructions are responsible for enforcing that a user
    can only delete their own queries before calling this tool.

    Args:
        query_name: The name of the query to delete.
        tool_context: The context provided by the ADK.

    Returns:
        True if the deletion was successful.

    Raises:
        ValueError: If no query with the given name is found to delete.
    """
    queries_ref = db.collection(query_collection)
    query = queries_ref.where("name", "==", query_name).limit(1)
    docs = list(query.stream())

    if not docs:
        raise ValueError(f"Query with name '{query_name}' not found to delete.")

    doc_id_to_delete = docs[0].id
    queries_ref.document(doc_id_to_delete).delete()

    return True