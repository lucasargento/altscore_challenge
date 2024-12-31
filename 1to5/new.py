data = "a01b01c01d01e01f01g01h01|a02b02c02d$2e02f02g02h02|a^3b03c$3d03e03f03g03h03|a04b04c$4d04e04f04g04h04|a05b05c05d05e05f05g05h05|a06b06c06d$6e06f06g06h06|a07b07c07d07e07f07g07h07|a08b08c08d08e#8f08g08h08|"

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

def print_grid(grid):
    print("Last movement:\n")
    for row in grid:
        print(" ".join(row))


grid = radar_to_grid(data)
print_grid(grid)