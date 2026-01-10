import requests

base_url = "https://pokeapi.co/api/v2/"

def get_pokemon_data(pokemon_name):
    """Fetches data for a given Pokémon by name."""
    url = f"{base_url}pokemon/{pokemon_name.lower()}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": "network error", "detail": str(e)}



def battle_pokemon_logic(pokemon1_name, pokemon2_name):
    """
    Execute battle logic and return result as dict.
    Winner determined by attack stat comparison.
    Used by backend API.
    """
    pokemon1_info = get_pokemon_data(pokemon1_name)
    pokemon2_info = get_pokemon_data(pokemon2_name)

    if "error" in pokemon1_info or "error" in pokemon2_info:
        return {"error": "Pokémon not found"}

    # Safely get stats
    stats1 = {s["stat"]["name"]: s["base_stat"] for s in pokemon1_info.get("stats", [])}
    stats2 = {s["stat"]["name"]: s["base_stat"] for s in pokemon2_info.get("stats", [])}

    pokemon1_attack = stats1.get("attack", 0)
    pokemon2_attack = stats2.get("attack", 0)

    if pokemon1_attack > pokemon2_attack:
        return {
            "winner": pokemon1_name,
            "loser": pokemon2_name,
            "winner_attack": pokemon1_attack,
            "loser_attack": pokemon2_attack
        }
    elif pokemon2_attack > pokemon1_attack:
        return {
            "winner": pokemon2_name,
            "loser": pokemon1_name,
            "winner_attack": pokemon2_attack,
            "loser_attack": pokemon1_attack
        }
    else:
        return {"error": "It's a tie! Try again."}

if __name__ == "__main__":
    import sys
    print("Testing battle logic...")
    result = battle_pokemon_logic("pikachu", "charizard")
    print(result)
