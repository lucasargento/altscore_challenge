import requests
from tqdm import tqdm 
import asyncio
import aiohttp


def get_all_poke_types():
    response = requests.get("https://pokeapi.co/api/v2/type/?offset=0&limit=100")
    data = response.json()
    results = data["results"]
    requested_types = {
        "bug": 0,
        "dark": 0,
        "dragon": 0,
        "electric": 0,
        "fairy": 0,
        "fighting": 0,
        "fire": 0,
        "flying": 0,
        "ghost": 0,
        "grass": 0,
        "ground": 0,
        "ice": 0,
        "normal": 0,
        "poison": 0,
        "psychic": 0,
        "rock": 0,
        "steel": 0,
        "water": 0
    }

    names = [result["name"] for result in results]
    names.sort()
    poke_types = []
    for data in data["results"]:
        name = data["name"]
        if name in requested_types.keys():
            print(name, "is ok")
            poke_types.append(data)
        else:
            print(name, "is not needed")
    print("All names:", names)
    print("requested names:", requested_types.keys())
    print("Returning data for ", len(poke_types), "poke types")
    print("Expected structure is:", poke_types[0])
    return poke_types

async def fetch_pokemon_height(session, url):
    async with session.get(url) as response:
        data = await response.json()
        return data["height"]

async def get_pokes_from_type(types):
    response_map = {}
    async with aiohttp.ClientSession() as session:
        for poke_type in types:
            print("Calculating for type:", poke_type["name"])
            async with session.get(poke_type["url"]) as response:
                data = await response.json()
                type_pokemons = data["pokemon"]
                poke_height_sum = 0
                tasks = []
                for pokemon in type_pokemons:
                    data_url = pokemon["pokemon"]["url"]
                    tasks.append(fetch_pokemon_height(session, data_url))
                heights = await asyncio.gather(*tasks)
                poke_height_sum = sum(heights)
                response_map[poke_type["name"]] = round(poke_height_sum / len(type_pokemons), 3)
                print("Average height for type:", poke_type["name"], "is", round(poke_height_sum / len(type_pokemons), 3))
    return response_map

# types = get_all_poke_types()
# result = asyncio.run(get_pokes_from_type(types))
# print(result)


API_KEY = "fa321ba8711540669f7af642453c7762"

# Encabezados con la clave de API
HEADERS = {
    "API-KEY": f"{API_KEY}",
    "Content-Type": "application/json"
}

def send_solution():
    """
    Envía la solución calculada.
    """
    payload = {
        "heights":{"normal": 15.665, "fighting": 22.6, "flying": 16.597, "poison": 33.706, "ground": 19.323, "rock": 18.02, "bug": 19.529, "ghost": 14.728, "steel": 27.758, "fire": 28.99, "water": 22.758, "grass": 16.822, "electric": 16.491, "psychic": 16.206, "ice": 18.273, "dragon": 43.374, "dark": 20.064, "fairy": 19.41}
    }
    response = requests.post("https://makers-challenge.altscore.ai/v1/s1/e6/solution", json=payload, headers=HEADERS)
    if response.status_code == 200:
        print("Solución enviada correctamente:", response.json())
    else:
        print("Error al enviar la solución:", response.text)

send_solution()