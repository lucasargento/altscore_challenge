import requests

SUBMIT_URL = "https://makers-challenge.altscore.ai/v1/s1/e4/solution"

# Clave de API
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
        "username": "Not all those who wander",
        "password": "are lost"
        }
    response = requests.post(SUBMIT_URL, json=payload, headers=HEADERS)
    if response.status_code == 200:
        print("Solución enviada correctamente:", response.json())
    else:
        print("Error al enviar la solución:", response.text)

if __name__ == "__main__":
    send_solution()