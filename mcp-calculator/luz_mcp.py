from mcp.server.fastmcp import FastMCP
import requests
import ast
import colorsys
from typing import Optional

mcp = FastMCP("ZzPet_Luz")

# Dirección URL donde se ejecuta traductor.py.
# Si lo ejecutas en la misma máquina, usa "http://127.0.0.1:8080".
# Si está en otro ordenador de tu red local, pon su IP (ej: "http://192.168.1.X:8080").
BASE_URL = "http://127.0.0.1:8080"

# Mapa inverso de hue a nombre de color (coincide con COLORES de traductor.py)
_HUES_A_COLOR = {0: "rojo", 30: "naranja", 60: "amarillo", 120: "verde",
                 180: "cian", 240: "azul", 280: "morado", 320: "rosa"}

def _parsear_estado():
    """Obtiene y parsea el estado actual de la tira LED.
    Devuelve (color_actual, brillo_actual) donde brillo es 1-100."""
    r = requests.get(f"{BASE_URL}/luz/estado", timeout=5)
    estado = ast.literal_eval(r.text)
    dps = estado.get("dps", {})
    modo = dps.get("21", "white")
    if modo == "colour":
        color_hex = dps.get("24", "")
        if len(color_hex) >= 12:
            h = int(color_hex[0:4], 16)
            s = int(color_hex[4:8], 16)
            v = int(color_hex[8:12], 16)
            brillo = max(1, min(100, v // 10))
            color = _HUES_A_COLOR.get(h)
            if color is None:
                # Color personalizado: convertir HSV a RGB hex (brillo máximo para color puro)
                r_f, g_f, b_f = colorsys.hsv_to_rgb(h / 360, s / 1000, 1.0)
                color = f"{int(r_f * 255):02x}{int(g_f * 255):02x}{int(b_f * 255):02x}"
            return color, brillo
    # Modo blanco o fallback
    brillo_raw = dps.get("22", 1000)
    return "blanco", max(1, min(100, brillo_raw // 10))

@mcp.tool()
def encender_luz() -> str:
    """Enciende la tira LED conectada al servidor traductor.py"""
    try:
        r = requests.get(f"{BASE_URL}/luz/on", timeout=5)
        return f"Respuesta: {r.text}"
    except Exception as e:
        return f"Error al encender la luz: {e}"

@mcp.tool()
def apagar_luz() -> str:
    """Apaga la tira LED conectada al servidor traductor.py"""
    try:
        r = requests.get(f"{BASE_URL}/luz/off", timeout=5)
        return f"Respuesta: {r.text}"
    except Exception as e:
        return f"Error al apagar la luz: {e}"

@mcp.tool()
def cambiar_brillo(porcentaje: int) -> str:
    """Ajusta el brillo de la tira LED (porcentaje de 1 a 100), manteniendo el modo y color actual."""
    try:
        color_actual, _ = _parsear_estado()
        if color_actual == "blanco":
            r = requests.get(f"{BASE_URL}/luz/brillo/{porcentaje}", timeout=5)
        else:
            r = requests.get(f"{BASE_URL}/luz/color/{color_actual}/{porcentaje}", timeout=5)
        return f"Respuesta: {r.text}"
    except Exception as e:
        return f"Error al cambiar brillo: {e}"

@mcp.tool()
def cambiar_color(color: str, brillo: Optional[int] = None) -> str:
    """Cambia el color de la tira LED.
    
    Parámetros:
    - color: Nombre del color (ej: 'rojo', 'naranja', 'amarillo', 'verde', 'cian', 'azul', 'morado', 'rosa', 'blanco') o un código Hexadecimal RGB de 6 caracteres (ej: 'FF0000').
    - brillo: (Opcional) Nivel de brillo entre 1 y 100. Si no se especifica, conserva el brillo actual.
    """
    try:
        if brillo is None:
            _, brillo = _parsear_estado()
        r = requests.get(f"{BASE_URL}/luz/color/{color}/{brillo}", timeout=5)
        return f"Respuesta: {r.text}"
    except Exception as e:
        return f"Error al cambiar color: {e}"

@mcp.tool()
def obtener_estado_luz() -> str:
    """Obtiene el estado actual de la tira LED."""
    try:
        r = requests.get(f"{BASE_URL}/luz/estado", timeout=5)
        return f"Estado actual: {r.text}"
    except Exception as e:
        return f"Error al obtener estado: {e}"

if __name__ == "__main__":
    mcp.run(transport="stdio")