import serial
import requests
import time

# --- CONFIGURACIÓN ---
# PUERTO: Puerto serial asignado a tu ESP32 / MiauMiau (ejemplo en Windows: "COM3", "COM5", etc.)
PUERTO = "COM_DE_TU_DISPOSITIVO"
BAUD = 115200

# TRADUCTOR_URL: Dirección donde corre 'traductor.py' (ej: "http://127.0.0.1:8080/luz/")
TRADUCTOR_URL = "http://127.0.0.1:8080/luz/"


# Frases que disparan acciones (ajústalas a cómo le hablas a MiauMiau)
ACCIONES = {
    "enciende la luz":       "on",
    "apaga la luz":          "off",
    "luz azul":              "color/azul",
    "luz roja":              "color/rojo",
    "brillo cincuenta":      "brillo/50",
}

print(f"Escuchando a MiauMiau en {PUERTO}...")
ser = serial.Serial(PUERTO, BAUD, timeout=1)
buffer = ""

try:
    while True:
        linea = ser.readline().decode("utf-8", errors="ignore").strip()
        if linea:
            buffer += linea + " "
            if len(buffer) > 500:
                buffer = buffer[-300:]
            
            texto = buffer.lower()
            for frase, accion in ACCIONES.items():
                if frase in texto:
                    print(f"✅ Detectada: '{frase}' → llamando a /{accion}")
                    try:
                        r = requests.get(TRADUCTOR_URL + accion, timeout=3)
                        print(f"   Respuesta del traductor: {r.text}")
                    except Exception as e:
                        print(f"    Error al llamar al traductor: {e}")
                    buffer = ""
except KeyboardInterrupt:
    print("\nDetenido.")
finally:
    ser.close()