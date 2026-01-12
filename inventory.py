def build_inventory(ingredient_list):
    inventory = {}

    for ingredient in ingredient_list:
        if ingredient in inventory:
            inventory[ingredient] += 1
        else:
            inventory[ingredient] = 1
    
    return inventory

def can_make_recipe(recipe, inventory):
    for ingredient in recipe["ingredients"]:
        if ingredient not in inventory or inventory[ingredient] <= 0:
            return False
    return True


def use_ingredients(recipe, inventory):
    for ingredient in recipe["ingredients"]:
        inventory[ingredient] -= 1


def match_recipes_with_inventory(inventory, recipes, threshold = 0.7):
    user_set = set(inventory.keys())
    matched_recipes = []

    for recipe in recipes:
        recipe_ingredients = set(recipe["ingredients"])
        matched = user_set.intersection(recipe_ingredients)

        score = len(matched) / len(recipe_ingredients)

        if score >= threshold and can_make_recipe(recipe, inventory):
            matched_recipes.append({
                "name": recipe["name"],
                "ingredients":recipe["ingredients"],
                "score": round(score, 2),
                "protein": recipe["protein"],
                "cook_time":recipe["cook_time"]
            })
    matched_recipes.sort(key = lambda x: x["score"], reverse = True)
    return matched_recipes
