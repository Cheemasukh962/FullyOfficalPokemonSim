#!/usr/bin/env python3
"""
API Testing Examples for Pokémon Battle Arena
Run this script to test all endpoints locally
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def print_header(title):
    """Print formatted section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def test_pokemon_endpoint():
    """Test GET /api/pokemon/<name>"""
    print_header("Test 1: Fetch Pokémon Data")
    
    pokemon_names = ["pikachu", "charizard", "blastoise"]
    
    for name in pokemon_names:
        url = f"{BASE_URL}/api/pokemon/{name}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {name.upper()}")
                print(f"   - Total Stats: {sum(s['base_stat'] for s in data['stats'])}")
                print(f"   - Types: {[t['type']['name'] for t in data['types']]}")
            else:
                print(f"❌ {name.upper()}: {response.status_code}")
        except Exception as e:
            print(f"❌ {name.upper()}: {str(e)}")

def test_battle_endpoint():
    """Test POST /api/battle"""
    print_header("Test 2: Battle Endpoint")
    
    battles = [
        ("pikachu", "charizard"),
        ("blastoise", "venusaur"),
        ("dragonite", "alakazam"),
    ]
    
    for pokemon1, pokemon2 in battles:
        url = f"{BASE_URL}/api/battle"
        payload = {
            "pokemon1": pokemon1,
            "pokemon2": pokemon2
        }
        
        try:
            response = requests.post(
                url,
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"⚔️  {pokemon1.upper()} vs {pokemon2.upper()}")
                print(f"   🏆 Winner: {data['winner'].upper()}")
                print(f"   📊 Winner Stats: {data['winner_stats']}")
                print(f"   ✨ Type Multiplier: {data['winner_multiplier']}x")
                print(f"   🎮 Battle ID: {data['battle_id']}\n")
            else:
                print(f"❌ Battle failed: {response.status_code}")
                print(f"   Error: {response.json()}\n")
        except Exception as e:
            print(f"❌ Error: {str(e)}\n")

def test_stats_endpoint():
    """Test GET /api/stats"""
    print_header("Test 3: Statistics Endpoint")
    
    # Get all stats
    url = f"{BASE_URL}/api/stats"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print(f"📊 Total Battles Recorded: {data['total_battles']}\n")
            
            if data['pokemon_wins']:
                print("🏆 Top Winners:")
                sorted_wins = sorted(
                    data['pokemon_wins'].items(),
                    key=lambda x: x[1],
                    reverse=True
                )
                for pokemon, wins in sorted_wins[:5]:
                    print(f"   {pokemon.upper()}: {wins} wins")
            
            print(f"\n📜 Recent Battles ({len(data['recent_battles'])} shown):")
            for battle in data['recent_battles'][:3]:
                print(f"   • {battle['winner'].upper()} defeated {battle['loser'].upper()}")
                print(f"     Stats: {battle['winner_stats']} vs {battle['loser_stats']}")
                print(f"     Time: {battle['created_at']}\n")
        else:
            print(f"❌ Failed to get stats: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_stats_with_filter():
    """Test GET /api/stats with filtering"""
    print_header("Test 4: Statistics with Filtering")
    
    pokemon = "pikachu"
    url = f"{BASE_URL}/api/stats?pokemon={pokemon}&limit=5"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print(f"🔍 Stats for {pokemon.upper()}")
            print(f"   Total battles (filtered): {data['total_battles']}")
            print(f"   Victories: {data['pokemon_wins'].get(pokemon, 0)}\n")
        else:
            print(f"❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_error_handling():
    """Test error handling"""
    print_header("Test 5: Error Handling")
    
    # Test 1: Invalid Pokémon
    print("Testing invalid Pokémon name...")
    try:
        response = requests.get(f"{BASE_URL}/api/pokemon/invalidpokemon123")
        if response.status_code == 404:
            print("✅ Correctly returns 404 for invalid Pokémon\n")
        else:
            print(f"❌ Expected 404, got {response.status_code}\n")
    except Exception as e:
        print(f"❌ Error: {str(e)}\n")
    
    # Test 2: Missing battle parameters
    print("Testing missing battle parameters...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/battle",
            json={"pokemon1": "pikachu"},  # Missing pokemon2
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 400:
            print("✅ Correctly returns 400 for missing parameters\n")
        else:
            print(f"❌ Expected 400, got {response.status_code}\n")
    except Exception as e:
        print(f"❌ Error: {str(e)}\n")
    
    # Test 3: Tie scenario (same Pokémon)
    print("Testing tie scenario...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/battle",
            json={"pokemon1": "pikachu", "pokemon2": "pikachu"},
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 409:
            print("✅ Correctly returns 409 for tie\n")
        else:
            print(f"❌ Expected 409, got {response.status_code}\n")
    except Exception as e:
        print(f"❌ Error: {str(e)}\n")

def test_database_persistence():
    """Test that battles are persisted"""
    print_header("Test 6: Database Persistence")
    
    print("Running 3 battles and verifying they're stored...\n")
    
    # Get initial count
    response1 = requests.get(f"{BASE_URL}/api/stats")
    initial_count = response1.json()['total_battles'] if response1.status_code == 200 else 0
    
    print(f"Initial battle count: {initial_count}")
    
    # Run a battle
    requests.post(
        f"{BASE_URL}/api/battle",
        json={"pokemon1": "squirtle", "pokemon2": "charmander"},
        headers={"Content-Type": "application/json"}
    )
    
    # Check count increased
    response2 = requests.get(f"{BASE_URL}/api/stats")
    final_count = response2.json()['total_battles'] if response2.status_code == 200 else 0
    
    print(f"Final battle count: {final_count}")
    
    if final_count > initial_count:
        print(f"✅ Battle persisted! Count increased by {final_count - initial_count}")
    else:
        print("❌ Battle was not persisted")

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("  POKÉMON BATTLE ARENA - API TEST SUITE")
    print("  Testing endpoints at: " + BASE_URL)
    print("  " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("="*60)
    
    try:
        # Test connectivity
        response = requests.get(f"{BASE_URL}/api/pokemon/pikachu", timeout=5)
        print("✅ Server is running and accessible\n")
    except Exception as e:
        print(f"❌ Cannot connect to server: {str(e)}")
        print("Make sure the Flask server is running:")
        print("   python source/api/server.py")
        return
    
    # Run all tests
    test_pokemon_endpoint()
    test_battle_endpoint()
    test_stats_endpoint()
    test_stats_with_filter()
    test_error_handling()
    test_database_persistence()
    
    print("\n" + "="*60)
    print("  TEST SUITE COMPLETE")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
