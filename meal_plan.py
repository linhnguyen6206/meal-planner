from inventory import can_make_recipe, use_ingredients

def inventory_usage_score(recipe, inventory):
    score = 0
    for ingredient in recipe["ingredients"]:
        if ingredient in inventory and inventory[ingredient] > 0:
            score += 1
    return score


def generate_weekly_plan(inventory, recipes):
    weekly_plan = []
    last_protein = None

    for day in range(7):
        feasible_recipes = []

        for recipe in recipes:
            if can_make_recipe(recipe, inventory):
                feasible_recipes.append(recipe)
        
        if not feasible_recipes:
            break

        feasible_recipes.sort(
            key = lambda r: inventory_usage_score(r, inventory),
            reverse = True
        )

        chosen_recipe = None

        for recipe in feasible_recipes:
            if recipe["protein"] != last_protein:
                chosen_recipe = recipe
                break

            if chosen_recipe is None:
                chosen_recipe = feasible_recipes[0]

            use_ingredients(chosen_recipe, inventory)

            weekly_plan.append({
                "day": f"Day {day + 1}",
                "meal": chosen_recipe["name"],
                "protein": chosen_recipe["protein"]
            })

            last_protein = chosen_recipe["protein"]

        return weekly_plan
