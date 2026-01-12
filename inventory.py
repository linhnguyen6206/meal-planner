def build_inventory(ingredient_list):
    inventory = {}
    for ingredient in ingredient_list:
        if ingredient in inventory:
            inventory[ingredient] += 1
        else:
            inventory[ingredient] = 1
    return inventory

def can_make_recipe(recipe, inventory):
    missing_count = 0
    for ingredient in recipe["ingredients"]:
        if ingredient not in inventory or inventory[ingredient] <= 0:
            missing_count += 1
    
    return missing_count <= 2

def use_ingredients(recipe, inventory):
    for ingredient in recipe["ingredients"]:
        # --- SAFER LOGIC ---
        # Only subtract the ingredient if we actually have it.
        # This prevents crashes when "can_make_recipe" lets us cook
        # something we don't fully have.
        if ingredient in inventory and inventory[ingredient] > 0:
            inventory[ingredient] -= 1

# Note: The function match_recipes_with_inventory is not used by your API,
# but we keep it here to avoid breaking imports if you use it elsewhere.
def match_recipes_with_inventory(inventory, recipes, threshold = 0.7):
    user_set = set(inventory.keys())
    matched_recipes = []
    for recipe in recipes:
        recipe_ingredients = set(recipe["ingredients"])
        matched = user_set.intersection(recipe_ingredients)
        score = len(matched) / len(recipe_ingredients)
        if score >= threshold:
            matched_recipes.append(recipe)
    return matched_recipes
