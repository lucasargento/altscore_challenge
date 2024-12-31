import requests
import math

# URL de la API
API_GET_URL = "https://makers-challenge.altscore.ai/v1/s1/e1/resources/measurement"
API_POST_URL = "https://makers-challenge.altscore.ai/v1/s1/e1/solution"

# Clave de API
API_KEY = "fa321ba8711540669f7af642453c7762"

# Encabezados con la clave de API
HEADERS = {
    "API-KEY": f"{API_KEY}",
    "Content-Type": "application/json"
}

def get_measurement():
    """
    Solicita mediciones del scanner hasta conseguir una medicion valida.
    """
    response = requests.get(API_GET_URL, headers=HEADERS)
    data = response.json()
    retries = 1
    try:
        while data["distance"] == 'failed to measure, try again':
            response = requests.get(API_GET_URL, headers=HEADERS)
            data = response.json()
            retries += 1
            print("Recibiendo respuesta del scanner:", data, "Intentos:", retries)
        return data.get("distance"), data.get("time")
    except Exception as e:
        print("Error al obtener datos del escáner:", e)
        raise Exception(f"Error al obtener datos del escáner: {response.status_code}, {response.text}")

def calculate_orbital_velocity(distance, time):
    """
    Calcula la velocidad orbital instantánea (en unidades astronómicas por hora).
    """
    if time == 0:
        raise ValueError("El tiempo no puede ser 0.")
    return round(distance / time)

def send_solution(velocity):
    """
    Envía la solución calculada a través de una solicitud POST.
    """
    payload = {"speed": velocity}
    response = requests.post(API_POST_URL, headers=HEADERS, json=payload)
    if response.status_code == 200:
        print("Solución enviada correctamente:", response.json())
    else:
        print(f"Error al enviar la solución: {response.status_code}, {response.text}")

def main():
    try:
        # Obtener los datos de la API
        distance, time = get_measurement()
        print(f"Datos obtenidos - Distancia: {distance}, Tiempo: {time}")
        
        # valido types
        distance = float(distance.split(" ")[0])
        time = float(time.split(" ")[0])

        # Calcular la velocidad orbital
        velocity = calculate_orbital_velocity(distance, time)
        print(f"Velocidad orbital calculada: {velocity} UA/h")

        # Enviar la solución
        send_solution(velocity)
    except Exception as e:
        print("Ocurrió un error:", e)

if __name__ == "__main__":
    main()
