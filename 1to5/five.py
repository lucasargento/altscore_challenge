import requests


starter_url = "https://makers-challenge.altscore.ai/v1/s1/e5/actions/start"
turn_url = "https://makers-challenge.altscore.ai/v1/s1/e5/actions/perform-turn"

# Clave de API
API_KEY = "fa321ba8711540669f7af642453c7762"

# Encabezados con la clave de API
HEADERS = {
    "API-KEY": f"{API_KEY}",
    "Content-Type": "application/json"
}

def radar_to_grid(radar_data):
    """
    Convierte el formato del radar en una cuadrícula 8x8.

    Args:
        radar_data (str): Cadena con el formato del radar.

    Returns:
        list[list[str]]: Matriz 8x8 con los valores del radar.
    """
    rows = radar_data.split("|")[:-1] # Separar las filas y eliminar el último separador vacío
    rows.reverse() # Invertir las filas para que la primera fila sea la de arriba
    grid = []
    for row in rows:
        # Tomar cada celda en la fila (3 caracteres por celda) y quedarnos con el segundo carácter
        grid.append([row[i+1] for i in range(0, len(row), 3)])
    return grid

def find_position(grid, char):
    """Encuentra la posición (fila, columna) de un carácter en la cuadrícula."""
    letras = ["a", "b", "c", "d", "e", "f", "g", "h"]
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == char:
                return letras[i]+str(j+1)
    return None

def print_grid(grid):
    print("Last movement:\n")
    for row in grid:
        print(" ".join(row))

# Datos del radar
bitacora_data = (
    "a01b01c01d01e01f01g01h01|a02b02c02d02e$2f02g02h02|a03b03c03d03e03f03g03h$3|a04b04c04d04e04f04g04h04|a05b05c05d05e$5f05g^5h05|a06b06c06d06e$6f06g06h06|a07b07c07d07e07f07g07h07|a08b08c08d08e08f#8g08h08|"
)
#Parsing inicial

def perform_turn(action, x_coord="a", y_coord="1"):
    payload = {
        "action": action,
        "attack_position": {
            "x": x_coord,
            "y": y_coord
        }
    }
    response = requests.post(turn_url, json=payload, headers=HEADERS)
    if response.status_code == 200:
        print(f"Performed turn action: {action}", response.json())
        return response.json()["action_result"]
    else:
        print("Error al enviar la solución:", response.text)

if __name__ == "__main__":
    starter = input("\nAre you ready to start? y/n:")
    if starter == "y":
        print("Let's start the game!")

        if True:
            print("succesfully starting")
            grid = radar_to_grid(bitacora_data)
            print_grid(grid)

            enemy_pos = find_position(grid, "^")
            friend_pos = find_position(grid, "#")

            for turn in range(4):
                print(f"\nTurno {turn}")
                print(f"- Enemigo en {enemy_pos}")
                print(f"- Aliado en {friend_pos}")
                
                action = input("action turn: attack/radar (a/r)")

                if action == "a":
                    print("attacking")
                    x_pos = str(input("Enter x position to attack (a-h):"))
                    y_pos = int(input("Enter y position to attack (1-8):"))

                    perform_turn(action="attack", x_coord=x_pos, y_coord=y_pos)
                else:
                    print("getting radar reading")
                    radar_data = perform_turn(action="radar")
                    grid = radar_to_grid(radar_data)
                    print_grid(grid)

                    enemy_pos = find_position(grid, "^")
                    friend_pos = find_position(grid, "#")
        else:
            print("\nExiting game")
            exit()
    else:
        print("\nExiting game")
        exit()

