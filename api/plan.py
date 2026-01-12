from http.server import BaseHTTPRequestHandler
import json
import os
import sys

def normalize(text):
    """Converts 'Chicken Breast ' to 'chicken breast' for easier matching."""
    return text.lower().strip()

def is_ingredient_available(recipe_ingredient, user_inventory):
    """
    Fuzzy Match: Returns True if the user has something similar.
    """
    recipe_item = normalize(recipe_ingredient)
    
    for user_item in user_inventory:
        user_item = normalize(user_item)
        # Check if one string is inside the other (Partial Match)
        if user_item in recipe_item or recipe_item in user_item:
            return True
    return False

def calculate_match_score(recipe, user_ingredients):
    """
    Returns a score (0.0 to 1.0) of how many ingredients the user has.
    """
    match_count = 0
    total_ingredients = len(recipe["ingredients"])
    
    if total_ingredients == 0:
        return 0

    for item in recipe["ingredients"]:
        if is_ingredient_available(item, user_ingredients):
            match_count += 1
            
    return match_count / total_ingredients

# --- MAIN HANDLER ---

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # 1. Receive Data
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            
            user_ingredients = data.get("ingredients", [])
            
            # 2. Load Recipes
            # We look for recipes.json in the main folder
            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)
            path_to_recipes = os.path.join(parent_dir, 'recipes.json')
            
            with open(path_to_recipes, 'r') as f:
                recipes = json.load(f)

            # 3. Generate Plan (Smart Mode)
            weekly_plan = []
            
            # Filter for recipes where we have at least 50% of ingredients
            feasible_recipes = []
            for recipe in recipes:
                score = calculate_match_score(recipe, user_ingredients)
                # If we have more than 30% of ingredients, consider it a match
                if score > 0.3: 
                    feasible_recipes.append(recipe)

            # If no matches, fallback to showing ANY recipe (so screen isn't empty)
            if not feasible_recipes:
                print("No strict matches found. Showing random suggestions.")
                feasible_recipes = recipes[:7]

            # Create 7 Day Plan
            import random
            random.shuffle(feasible_recipes) # Shuffle so it's not the same every day
            
            # Cycle through the feasible recipes to fill 7 days
            for i in range(7):
                # Use modulo operator % to loop back to start of list if we run out
                recipe = feasible_recipes[i % len(feasible_recipes)]
                
                weekly_plan.append({
                    "day": f"Day {i + 1}",
                    "meal": recipe["name"],
                    "protein": recipe.get("protein", "Variety")
                })

            # 4. Send Response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(weekly_plan).encode('utf-8'))

        except Exception as e:
            # Error Handling
            print(f"CRITICAL ERROR: {e}")
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
