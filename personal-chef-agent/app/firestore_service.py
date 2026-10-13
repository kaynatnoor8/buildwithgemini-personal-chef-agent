"""Firestore database helpers and client setup for personal-chef-agent."""

import logging
from typing import Any, Dict, List, Optional
from google.cloud import firestore

logger = logging.getLogger(__name__)

# Hardcoded project ID as string to prevent issues on Agent Platform deployments
PROJECT_ID = "qwiklabs-gcp-04-b54b139415f4"
RECIPES_COLLECTION = "recipes"

_db: Optional[firestore.Client] = None


def get_firestore_client() -> firestore.Client:
    """Returns a singleton Firestore client configured with the hardcoded project ID."""
    global _db
    if _db is None:
        _db = firestore.Client(project=PROJECT_ID)
    return _db


def search_recipes(
    cuisine: Optional[str] = None,
    dietary_tag: Optional[str] = None,
    max_prep_time_minutes: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """Search or list recipes in the catalog matching specified criteria.

    Args:
        cuisine: Optional cuisine filter (e.g. 'Italian', 'Mexican', 'Japanese', 'Mediterranean').
        dietary_tag: Optional dietary restriction/tag to match (e.g. 'vegetarian', 'vegan', 'gluten-free', 'keto', 'high-protein').
        max_prep_time_minutes: Optional maximum prep and cooking time in minutes.

    Returns:
        A list of matching recipe dictionaries containing recipe details.
    """
    db = get_firestore_client()
    recipes_ref = db.collection(RECIPES_COLLECTION)
    docs = recipes_ref.stream()

    results: List[Dict[str, Any]] = []
    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id

        if cuisine and data.get("cuisine", "").lower() != cuisine.lower():
            continue

        if dietary_tag:
            tags = [t.lower() for t in data.get("dietary_tags", [])]
            if dietary_tag.lower() not in tags:
                continue

        if max_prep_time_minutes is not None:
            total_time = data.get("prep_time_minutes", 0) + data.get("cook_time_minutes", 0)
            if total_time > max_prep_time_minutes:
                continue

        results.append(data)

    return results


def get_recipe_by_id(recipe_id: str) -> Dict[str, Any]:
    """Retrieve full details of a recipe by its document ID.

    Args:
        recipe_id: The unique identifier of the recipe.

    Returns:
        The recipe details dictionary or an error message if not found.
    """
    db = get_firestore_client()
    doc = db.collection(RECIPES_COLLECTION).document(recipe_id).get()
    if not doc.exists:
        return {"error": f"Recipe with ID '{recipe_id}' not found."}

    data = doc.to_dict()
    data["id"] = doc.id
    return data


def add_recipe(
    title: str,
    description: str,
    cuisine: str,
    servings: int,
    prep_time_minutes: int,
    cook_time_minutes: int,
    ingredients: List[str],
    instructions: List[str],
    dietary_tags: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Add a new recipe to the curated recipes catalog.

    Args:
        title: The recipe name (e.g. 'Classic Guacamole').
        description: Brief overview of the dish.
        cuisine: Cuisine type (e.g. 'Mexican', 'Italian').
        servings: Number of servings this recipe yields.
        prep_time_minutes: Preparation time in minutes.
        cook_time_minutes: Cooking time in minutes.
        ingredients: List of ingredients with quantities (e.g. ['3 ripe avocados', '1 lime, juiced']).
        instructions: Ordered step-by-step preparation and cooking instructions.
        dietary_tags: Optional list of dietary tags (e.g. ['vegan', 'gluten-free']).

    Returns:
        Confirmation dictionary with the generated recipe ID.
    """
    db = get_firestore_client()
    recipe_data = {
        "title": title,
        "description": description,
        "cuisine": cuisine,
        "servings": servings,
        "prep_time_minutes": prep_time_minutes,
        "cook_time_minutes": cook_time_minutes,
        "ingredients": ingredients,
        "instructions": instructions,
        "dietary_tags": dietary_tags or [],
        "created_at": firestore.SERVER_TIMESTAMP,
    }

    doc_ref = db.collection(RECIPES_COLLECTION).add(recipe_data)
    # doc_ref is a tuple: (timestamp, document_reference)
    created_id = doc_ref[1].id

    return {
        "status": "success",
        "message": f"Recipe '{title}' created successfully.",
        "id": created_id,
    }
