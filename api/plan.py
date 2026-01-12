from http.server import BaseHTTPRequestHandler
import json
import os
import sys

# --- THE FIX FOR THE 500 ERROR ---
# This forces Python to look in the main folder for your other files
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
# ---------------------------------

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # 1. Try to import your files here (inside the try block)
            # If this fails, we will catch the error below
            from inventory import build_inventory
            from meal_plan import generate_weekly_plan

            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)

            user_ingredients = data.get("ingredients", [])
            inventory = build_inventory(user_ingredients)

            # 2. Fix the path to recipes.json
            path_to_recipes = os.path.join(parent_dir, 'recipes.json')
            
            # Check if recipes.json actually exists
            if not os.path.exists(path_to_recipes):
                raise FileNotFoundError(f"Cannot find file at: {path_to_recipes}")

            with open(path_to_recipes, 'r') as f:
                recipes = json.load(f)

            plan = generate_weekly_plan(inventory, recipes)

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(plan).encode('utf-8'))

        except Exception as e:
            # --- ERROR REPORTER ---
            # If it crashes, this sends the specific error to your browser
            error_message = f"CRITICAL ERROR: {str(e)}"
            print(error_message) # Print to terminal
            
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"error": error_message}).encode('utf-8'))
