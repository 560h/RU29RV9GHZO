from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

app = Flask(__name__)

# Pokemon TCG API endpoint
POKEMON_TCG_API = "https://api.pokemontcg.io/v2"

def get_charizard_cards():
    # Fetch Charizard cards from Pokemon TCG API
    headers = {
        "X-Api-Key": "YOUR_API_KEY"  # You'll need to get an API key from pokemontcg.io
    }
    
    params = {
        "q": "name:Charizard",
        "orderBy": "-set.releaseDate",
        "select": "id,name,images,set,rarity,number,cardmarket",
        "pageSize": 100  # Get more cards per request
    }
    
    all_cards = []
    page = 1
    
    while True:
        params["page"] = page
        response = requests.get(f"{POKEMON_TCG_API}/cards", headers=headers, params=params)
        
        if response.status_code != 200:
            break
            
        data = response.json()
        cards = data.get("data", [])
        
        if not cards:
            break
            
        all_cards.extend(cards)
        page += 1
        
        # Break if we've reached the last page
        if page > data.get("totalCount", 0) // params["pageSize"] + 1:
            break
    
    # Sort cards by release date (newest first)
    all_cards.sort(key=lambda x: x.get("set", {}).get("releaseDate", ""), reverse=True)
    
    return all_cards

@app.route('/')
def index():
    cards = get_charizard_cards()
    return render_template('index.html', cards=cards)

if __name__ == '__main__':
    app.run(debug=True) 
