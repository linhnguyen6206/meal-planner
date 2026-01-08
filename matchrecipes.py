def match_recipes(user_ingredients, recipes, threshold=0.7):
    """
    Matches recipes based on available ingredients.

    Parameters:
        user_ingredients (list): ingredients the user has
        recipes (list): list of recipe dictionaries
        threshold (float): minimum match score to keep a recipe

    Returns:
        list of matched recipes with scores
    """

    # Convert user ingredients to a set for fast lookup
    user_set = set(user_ingredients)

    matched_recipes = []

    for recipe in recipes:
        recipe_ingredients = set(recipe["ingredients"])

        # Find intersection
        matched = user_set.intersection(recipe_ingredients)

        # Calculate match score
        score = len(matched) / len(recipe_ingredients)

        # Keep recipes that meet threshold
        if score >= threshold:
            matched_recipes.append({
                "name": recipe["name"],
                "score": round(score, 2),
                "missing_ingredients": list(recipe_ingredients - user_set),
                "protein": recipe["protein"],
                "cook_time": recipe["cook_time"]
            })

    # Sort recipes by best match first
    matched_recipes.sort(key=lambda x: x["score"], reverse=True)

    return matched_recipes
