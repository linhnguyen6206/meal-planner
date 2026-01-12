from http.server import BaseHTTPRequestHandler
import json
import os
import sys

# Standard logic to find your files
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            from inventory import build_inventory
            from meal_plan import generate_weekly_plan

            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)

            # --- FIX 1: CLEAN THE INPUT ---
            # Force everything to lowercase and remove spaces
            raw_ingredients = data.get("ingredients", [])
            cleaned_ingredients = [i.lower().strip() for i in raw_ingredients]
            
            print(f"User has: {cleaned_ingredients}") # This will show in Vercel Logs

            inventory = build_inventory(cleaned_ingredients)

            path_to_recipes = os.path.join(parent_dir, 'recipes.json')
            with open(path_to_recipes, 'r') as f:
                recipes = json.load(f)

            # --- FIX 2: DEBUG THE MATCHING ---
            plan = generate_weekly_plan(inventory, recipes)
            
            print(f"Generated {len(plan)} meals") # This will show in Vercel Logs

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(plan).encode('utf-8'))

        except Exception as e:
            print(f"ERROR: {e}")
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
