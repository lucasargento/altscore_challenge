import requests
from tqdm import tqdm

# URLs base para obtener datos
HOLOCRON_PEOPLE_URL = "https://www.swapi.tech/api/people?page=1&limit=100"
SUBMIT_URL = "https://makers-challenge.altscore.ai/v1/s1/e3/solution"

# Clave de API
API_KEY = "fa321ba8711540669f7af642453c7762"

# Encabezados con la clave de API
HEADERS = {
    "API-KEY": f"{API_KEY}",
    "Content-Type": "application/json"
}

def send_solution(planet_name):
    """
    Envía la solución calculada.
    """
    payload = {"planet": planet_name}
    response = requests.post(SUBMIT_URL, json=payload, headers=HEADERS)
    if response.status_code == 200:
        print("Solución enviada correctamente:", response.json())
    else:
        print("Error al enviar la solución:", response.text)


def get_holocron_people_data():
    """
    Obtiene los datos del holocrón sobre personajes y planetas.
    """
    response = requests.get(HOLOCRON_PEOPLE_URL)
    if response.status_code == 200:
        data = response.json()
        results = data.get("results")
        return [result["url"] for result in results]
    else:
        raise Exception(f"Error al obtener datos del holocrón: {response.text}")

def get_holocron_planet_data(planet_link):
    """
    Obtiene los datos del holocrón sobre personajes y planetas.
    """
    response = requests.get(planet_link)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        raise Exception(f"Error al obtener datos del holocrón: {response.text}")

def consultar_oraculo(name):
    """
    Consulta al oráculo para determinar el lado de la Fuerza del personaje.
    """
    response = requests.get(f"https://makers-challenge.altscore.ai/v1/s1/e3/resources/oracle-rolodex?name={name}", headers=HEADERS)
    if response.status_code == 200:
        code = response.json()["oracle_notes"]
        decoded = decodeBase64(code)
        if "Light Side" in decoded:
            return "luminoso"
        else:
            return "oscuro"
    else:
        raise Exception(f"Error al consultar el oráculo para {name}: {response.text}")

def calcular_ibf(planet_data):
    """
    Calcula el Índice de Balance de la Fuerza (IBF) para cada planeta.
    """
    
    for planeta, data in planet_data.items():
        num_luminoso = data["light_people"]
        num_oscuro = data["dark_people"]
        total_personajes = data["total"]

        if total_personajes == 0:
            ibf = "null"
        else:
            ibf = (num_luminoso - num_oscuro) / total_personajes
        planet_data[planeta]["IBF"] = ibf
    
    return planet_data

def encontrar_planeta_equilibrio(resultados_ibf):
    """
    Encuentra el planeta con IBF = 0 (equilibrio en la Fuerza).
    """
    chosen_planets = []
    for planeta, data in resultados_ibf.items():
        ibf = data["IBF"]
        if ibf == 0:
            chosen_planets.append(planeta)
    return chosen_planets

def decodeBase64(data):
    import base64
    decoded_text = base64.b64decode(data).decode('utf-8')
    return decoded_text

def create_planet_map():
    response = requests.get("https://www.swapi.tech/api/planets?page=1&limit=100")
    response = response.json()
    all_planets = response["results"]

    planet_map = {}
    for planet in all_planets:
        planet_map[planet["name"]] = {"id":planet["uid"], "light_people":0, "dark_people":0, "total":0, "IBF": "null"}
    return planet_map

def calculate_people_per_planet(people_links, planet_map):
    print("\n> Calculating people per planet\n")
    for person in tqdm(people_links):
        character_info = requests.get(person).json()
        character_name = character_info["result"]["properties"]["name"]
        
        homeworld_link = character_info["result"]["properties"]["homeworld"]
        planet_info = get_holocron_planet_data(homeworld_link)
        
        planet_name = planet_info["result"]["properties"]["name"]
        person_side = consultar_oraculo(character_name)
        
        if person_side == "luminoso":
            planet_map[planet_name]["light_people"] += 1
            planet_map[planet_name]["total"] += 1
        else:
            planet_map[planet_name]["dark_people"] += 1
            planet_map[planet_name]["total"] += 1
        
    return planet_map

def main():
    try:
        holocron__people_links = get_holocron_people_data()
        planet_map = create_planet_map()

        updated_planet_map = calculate_people_per_planet(holocron__people_links, planet_map)
        planet_map_ibf = calcular_ibf(updated_planet_map)
        planeta_equilibrio = encontrar_planeta_equilibrio(planet_map_ibf)
        chosenone = planeta_equilibrio[0]
        print("\nChosen planet!! ==> ", chosenone)
        send_solution(chosenone)
    except Exception as e:
        print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    main()
