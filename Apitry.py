import requests
import sys
import webbrowser

base_url = "https://pokeapi.co/api/v2/"
# IMPORTANT: Replace "YOUR_API_KEY_HERE" with your actual Giphy API key
GIPHY_API_KEY = "jx06m5LpswQ8q0HBeqHqeMvfH6bh1r26" 

def get_pokemon_data(pokemon_name):
    """Fetches data for a given Pokémon by name."""
    url = f"{base_url}pokemon/{pokemon_name.lower()}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": "network error", "detail": str(e)}

def print_pokemon_weight(pokemon_name):
    pokemon_info = get_pokemon_data(pokemon_name)
    if "error" in pokemon_info:
        print(f"Error: {pokemon_info.get('error')} (detail: {pokemon_info.get('detail')})")
    else:
        weight = pokemon_info.get("weight")
        print(f"{pokemon_name.title()} weight: {weight}")

def print_pokemon_abilities(pokemon_name):
    pokemon_info = get_pokemon_data(pokemon_name)
    if "error" in pokemon_info:
        print("Error fetching abilities.")
        return
    abilities = pokemon_info.get("abilities", [])
    print(f"{pokemon_name.title()} abilities:")
    for entry in abilities:
        ability_name = entry["ability"]["name"]
        hidden = entry["is_hidden"]
        print(f" - {ability_name}{' (hidden)' if hidden else ''}")

def print_pokemon_stats(pokemon_name):
    pokemon_info = get_pokemon_data(pokemon_name)
    if "error" in pokemon_info:
        print("Error fetching stats.")
        return
    print(f"{pokemon_name.title()} stats:")
    for every in pokemon_info.get("stats", []):
        stat_name = every["stat"]["name"]
        base_stat = every["base_stat"]
        print(f" - {stat_name}: {base_stat}")

def print_pokemon_height(pokemon_name):
    pokemon_info = get_pokemon_data(pokemon_name)
    if "error" in pokemon_info:
        print("Error fetching height.")
        return
    get_height = pokemon_info.get("height")
    print(f"{pokemon_name.title()} height: {get_height} (decimetres)")

def print_pokemon_types(pokemon_name):
    pokemon_info = get_pokemon_data(pokemon_name)
    if "error" in pokemon_info:
        print("Error fetching types.")
        return
    types = pokemon_info.get("types", [])
    print(f"{pokemon_name.title()} types:")
    for type_entry in types:
        type_name = type_entry["type"]["name"]
        print(f" - {type_name}")




def get_pokemon_gif(pokemon_name, api_key):
    """Fetches a GIF for a given Pokémon."""
    url = "https://api.giphy.com/v1/gifs/search"
    params = {
        "api_key": api_key,
        "q": pokemon_name,
        "limit": 1,
        "rating": "g"
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data["data"]:
            return data["data"][0]["images"]["original"]["url"]
        else:
            return "No GIF found."
    except requests.RequestException as e:
        return f"Could not fetch GIF: {e}"
    
    
    
    
    
def battle_pokemon(pokemon1_name, pokemon2_name):
    pokemon1_info = get_pokemon_data(pokemon1_name)
    pokemon2_info = get_pokemon_data(pokemon2_name)

    if "error" in pokemon1_info:
        print(f"Error: {pokemon1_name.title()} not found.")
        return
    if "error" in pokemon2_info:
        print(f"Error: {pokemon2_name.title()} not found.")
        return

    # Safely get stats
    stats1 = {s["stat"]["name"]: s["base_stat"] for s in pokemon1_info.get("stats", [])}
    stats2 = {s["stat"]["name"]: s["base_stat"] for s in pokemon2_info.get("stats", [])}

    pokemon1_attack = stats1.get("attack", 0)
    pokemon2_attack = stats2.get("attack", 0)
    
    print(f"\n--- BATTLE ---")
    print(f"{pokemon1_name.title()} Attack: {pokemon1_attack}")
    print(f"{pokemon2_name.title()} Attack: {pokemon2_attack}")

    winner_name = None
    search_term = None

    if pokemon1_attack > pokemon2_attack:
        winner_name = pokemon1_name
        print(f"\n{winner_name.title()} wins!")
        search_term = winner_name
    elif pokemon2_attack > pokemon1_attack:
        winner_name = pokemon2_name
        print(f"\n{winner_name.title()} wins!")
        search_term = winner_name
    else:
        print("\nIt's a tie!")
        search_term = f"{pokemon1_name} and {pokemon2_name} tie"

    print(f"Searching for a GIF for '{search_term}'...")
    gif_url = get_pokemon_gif(search_term, GIPHY_API_KEY)

    if gif_url and not gif_url.startswith("Could not fetch") and not gif_url.startswith("No GIF"):
        print(f"Opening GIF: {gif_url}")
        webbrowser.open(gif_url)
    else:
        print(gif_url) # Print error or "No GIF found"


if __name__ == "__main__":
    print("--- Pokémon Info And Battle ---")
    
    # Get Pokémon 1
    name1 = sys.argv[1] if len(sys.argv) > 1 else input("Enter first Pokémon name: ")
    if not name1:
        sys.exit("First Pokémon name is required.")
        
    print(f"\n--- {name1.title()}'s Info ---")
    print_pokemon_stats(name1)
    print_pokemon_types(name1)

    # Get Pokémon 2
    name2 = sys.argv[2] if len(sys.argv) > 2 else input("Enter second Pokémon name: ")
    if not name2:
        sys.exit("Second Pokémon name is required for battle.")

    print(f"\n--- {name2.title()}'s Info ---")
    print_pokemon_stats(name2)
    print_pokemon_types(name2)

    # Battle
    battle_pokemon(name1, name2)