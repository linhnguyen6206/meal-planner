import json
from collections import Counter

# ---- load recipes ----
with open("recipes.json") as f:
    recipes = json.load(f)

# ---- inventory helpers ----
def build_inventory(ingredients):
    return Counter(ingredients)

def can_make_recipe(recipe, inventory):
    for ingredient in recipe["ingredients"]:
        if inventory[ingredient] <= 0:
            return False
    return True

def use_ingredients(recipe, inventory):
    for ingredient in recipe["ingredients"]:
        inventory[ingredient] -= 1

def inventory_usage_score(recipe, inventory):
    return sum(1 for i in recipe["ingredients"] if inventory[i] > 0)

def generate_weekly_plan(inventory, recipes):
    plan = []
    last_protein = None

    for day in range(7):
        feasible = [r for r in recipes if can_make_recipe(r, inventory)]
        if not feasible:
            break

        feasible.sort(
            key=lambda r: inventory_usage_score(r, inventory),
            reverse=True
        )

        chosen = None
        for r in feasible:
            if r["protein"] != last_protein:
                chosen = r
                break

        if chosen is None:
            chosen = feasible[0]

        use_ingredients(chosen, inventory)
        plan.append({"day": f"Day {day+1}", "meal": chosen["name"]})
        last_protein = chosen["protein"]

    return plan

# ---- Vercel handler ----
def handler(request):
    if request.method != "POST":
        return {
            "statusCode": 405,
            "body": "Method not allowed"
        }

    data = json.loads(request.body)
    ingredients = [i.strip().lower() for i in data["ingredients"]]

    inventory = build_inventory(ingredients)
    weekly_plan = generate_weekly_plan(inventory, recipes)

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(weekly_plan)
    }
