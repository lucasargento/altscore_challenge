import requests
import math 
from tqdm import tqdm

# URLs de la API
API_GET_URL = "https://makers-challenge.altscore.ai/v1/s1/e2/resources/stars"
API_POST_URL = "https://makers-challenge.altscore.ai/v1/s1/e2/solution"

# Clave de API
API_KEY = "fa321ba8711540669f7af642453c7762"

# Encabezados con la clave de API
HEADERS = {
    "API-KEY": f"{API_KEY}",
    "Content-Type": "application/json"
}

def get_stars_data():
    """
    Navega por los saltos estelares para obtener datos de las estrellas.
    """
    all_resonances = []
    all_ids = []

    # seed response to get the total amount of stars
    response = requests.get(API_GET_URL, headers=HEADERS)
    if response.status_code == 200:
        total_stars = response.headers["x-total-count"]
        print("Total stars:", total_stars)
        total_iters = math.ceil(int(total_stars) / 3)
        print("Total iters needed:", total_iters)

    for iter in tqdm(range(0, total_iters)):    
        #print("Pidiendole al oraculo la informacion de las estrellas. Iteracion numero", iter+1)    
        payload = {
            "page": str(iter+1),
            "sort-by": "id",
            "sort-direction": "desc"
        }

        response = requests.get(API_GET_URL, headers=HEADERS, params=payload)
        if response.status_code == 200:
            data = response.json()
            headers = response.headers
            #print("susurros:", headers,"\n")
            #print("Recibiendo informacion de 3 estrellas del oraculo:\n", data, len(data))
            # Extraer resonancias
            resonances = [star["resonance"] for star in data]
            ids = [star["id"] for star in data]
            all_resonances.extend(resonances)
            all_ids.extend(ids)
        else:
            raise Exception(f"Error al obtener datos: {response.text}")

    print("Resonancias obtenidas:", all_resonances)
    print("Nombres de las estrellas:", all_ids)

    unique_stars = len(set(all_ids))
    print("Estrellas unicas:", unique_stars)
    return all_resonances

def calculate_average_resonance(resonances):
    """
    Calcula la resonancia promedio.
    """
    if not resonances:
        raise ValueError("No hay datos de resonancia.")
    return round(sum(resonances) / len(resonances))

def send_solution(average_resonance):
    """
    Envía la solución calculada.
    """
    payload = {"average_resonance": average_resonance}
    response = requests.post(API_POST_URL, json=payload, headers=HEADERS)
    if response.status_code == 200:
        print("Solución enviada correctamente:", response.json())
    else:
        print("Error al enviar la solución:", response.text)

def main():
    try:
        # Obtener los datos de las estrellas
        resonances = get_stars_data()
        print(f"Resonancias obtenidas: {resonances}")

        # Calcular la resonancia promedio
        average_resonance = calculate_average_resonance(resonances)
        print(f"Resonancia promedio calculada: {average_resonance}")

        # Enviar la solución
        send_solution(average_resonance)
    except Exception as e:
        print("Ocurrió un error:", e)

if __name__ == "__main__":
    main()
