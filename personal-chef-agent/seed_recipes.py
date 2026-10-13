#!/usr/bin/env python3
"""Seed script for personal-chef-agent Firestore recipe catalog."""

from google.cloud import firestore

# Hardcoded project ID as string
PROJECT_ID = "qwiklabs-gcp-04-b54b139415f4"
RECIPES_COLLECTION = "recipes"

SEED_RECIPES = [
    {
        "title": "Tuscan Garlic Herb Salmon",
        "description": "Pan-seared salmon fillet in a rich garlic, sun-dried tomato, and spinach cream sauce.",
        "cuisine": "Mediterranean",
        "servings": 2,
        "prep_time_minutes": 10,
        "cook_time_minutes": 15,
        "dietary_tags": ["keto", "gluten-free", "high-protein"],
        "ingredients": [
            "2 fresh salmon fillets (6 oz each)",
            "2 cloves garlic, minced",
            "1 cup fresh baby spinach",
            "1/3 cup sun-dried tomatoes, drained and sliced",
            "1/2 cup heavy cream or coconut cream",
            "1 tbsp olive oil",
            "Salt and freshly cracked black pepper to taste",
        ],
        "instructions": [
            "Season salmon fillets on both sides with salt and pepper.",
            "Heat olive oil in a skillet over medium-high heat. Sear salmon 4-5 minutes per side until golden. Set aside.",
            "In the same skillet, sauté garlic for 1 minute until fragrant.",
            "Add sun-dried tomatoes and spinach, cooking until spinach wilts.",
            "Pour in heavy cream, simmer for 2-3 minutes until thickened slightly.",
            "Return salmon to skillet, spoon sauce over fish, and serve immediately.",
        ],
    },
    {
        "title": "Creamy Coconut Chickpea Curry",
        "description": "Hearty, fragrant vegan curry packed with protein, tender chickpeas, and warm spices.",
        "cuisine": "Indian",
        "servings": 4,
        "prep_time_minutes": 10,
        "cook_time_minutes": 20,
        "dietary_tags": ["vegan", "vegetarian", "gluten-free", "dairy-free"],
        "ingredients": [
            "2 cans (15 oz each) chickpeas, rinsed and drained",
            "1 can (13.5 oz) full-fat coconut milk",
            "1 can (14 oz) diced tomatoes",
            "1 medium yellow onion, diced",
            "3 cloves garlic, minced",
            "1 tbsp fresh ginger, grated",
            "1.5 tbsp curry powder",
            "1 tsp ground cumin",
            "2 cups baby spinach",
            "1 tbsp coconut oil",
            "Fresh cilantro and lime wedges for garnish",
        ],
        "instructions": [
            "Heat coconut oil in a large pot over medium heat. Sauté onion until translucent (approx. 5 minutes).",
            "Add garlic, ginger, curry powder, and cumin. Stir for 1 minute until aromatic.",
            "Pour in diced tomatoes, coconut milk, and chickpeas. Stir well to combine.",
            "Bring to a gentle boil, then reduce heat and simmer uncovered for 15 minutes to allow flavors to meld.",
            "Fold in baby spinach until wilted (approx. 2 minutes).",
            "Garnish with fresh cilantro and a squeeze of fresh lime juice before serving.",
        ],
    },
    {
        "title": "Avocado & Black Bean Fiesta Salad",
        "description": "Crisp and colorful Southwestern salad tossed in a zesty cilantro lime vinaigrette.",
        "cuisine": "Mexican",
        "servings": 3,
        "prep_time_minutes": 15,
        "cook_time_minutes": 0,
        "dietary_tags": ["vegan", "vegetarian", "gluten-free"],
        "ingredients": [
            "2 ripe avocados, diced",
            "1 can (15 oz) black beans, rinsed and drained",
            "1 cup sweet corn kernels (fresh or thawed)",
            "1 cup cherry tomatoes, halved",
            "1/4 cup red onion, finely diced",
            "1/4 cup fresh cilantro, chopped",
            "2 tbsp extra virgin olive oil",
            "2 tbsp fresh lime juice",
            "1/2 tsp ground cumin",
            "Salt and chili powder to taste",
        ],
        "instructions": [
            "In a large salad bowl, combine black beans, sweet corn, cherry tomatoes, and red onion.",
            "In a small bowl, whisk together olive oil, lime juice, cumin, salt, and chili powder.",
            "Gently fold in diced avocado and chopped cilantro.",
            "Drizzle dressing over salad and toss gently to coat without mashing the avocados.",
            "Serve chilled or at room temperature.",
        ],
    },
    {
        "title": "Quick Lemon Herb Chicken Skillet",
        "description": "Tender chicken breasts pan-seared with rosemary, oregano, and a vibrant lemon butter glaze.",
        "cuisine": "American",
        "servings": 4,
        "prep_time_minutes": 10,
        "cook_time_minutes": 15,
        "dietary_tags": ["keto", "gluten-free", "high-protein", "low-carb"],
        "ingredients": [
            "4 boneless skinless chicken breasts, pounded to even thickness",
            "2 tbsp olive oil",
            "2 tbsp butter",
            "1 lemon, sliced into rounds plus 2 tbsp lemon juice",
            "3 cloves garlic, minced",
            "1 tsp dried oregano",
            "1 tsp fresh rosemary, minced",
            "Salt and black pepper to taste",
        ],
        "instructions": [
            "Pat chicken breasts dry with paper towels and season generously with salt, pepper, and oregano.",
            "Heat olive oil in a large skillet over medium-high heat. Add chicken and sear 6-7 minutes per side until internal temp reaches 165°F (74°C). Remove to a warm plate.",
            "Reduce heat to medium. Melt butter in the skillet, adding garlic, rosemary, and lemon juice. Cook for 1 minute.",
            "Add lemon slices to sear lightly in the pan for 1-2 minutes.",
            "Return chicken to pan, baste with pan sauce, and serve hot.",
        ],
    },
]


def seed():
    print(f"Connecting to Firestore with project '{PROJECT_ID}'...")
    db = firestore.Client(project=PROJECT_ID)
    recipes_ref = db.collection(RECIPES_COLLECTION)

    print(f"Seeding {len(SEED_RECIPES)} recipes into collection '{RECIPES_COLLECTION}'...")
    for recipe in SEED_RECIPES:
        doc_data = {**recipe, "created_at": firestore.SERVER_TIMESTAMP}
        _, ref = recipes_ref.add(doc_data)
        print(f"  ✓ Added '{recipe['title']}' (ID: {ref.id})")

    print("\nSeeding complete!")


if __name__ == "__main__":
    seed()
