from http.server import BaseHTTPRequestHandler
import json
import os

# Import your existing logic
from inventory import build_inventory
from meal_plan import generate_weekly_plan

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # 1. Read the length of the incoming data
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        # 2. Get ingredients from the user's input
        user_ingredients = data.get("ingredients", [])
        inventory = build_inventory(user_ingredients)

        # 3. Load your recipes database
        # In a Vercel environment, we use an absolute path for the JSON file
        path_to_recipes = os.path.join(os.path.dirname(__file__), '..', 'recipes.json')
        with open(path_to_recipes, 'r') as f:
            recipes = json.load(f)

        # 4. Generate the 7-day plan
        plan = generate_weekly_plan(inventory, recipes)

        # 5. Send the response back to index.html
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(plan).encode('utf-8'))