import tinytuya
import colorsys
from http.server import BaseHTTPRequestHandler, HTTPServer

# --- CONFIGURACIÓN DE TU DISPOSITIVO TUYA ---
# DEVICE_ID: Identificador único de tu dispositivo Tuya / Smart Life.
DEVICE_ID = "TU_DEVICE_ID_AQUI"

# IP_TIRA: Dirección IP local que tu router asignó a la tira LED (ej: "192.168.1.50").
IP_TIRA   = "TU_IP_LOCAL_DE_LA_TIRA"

# LOCAL_KEY: Clave de seguridad local de exactamente 16 caracteres de tu dispositivo Tuya.
LOCAL_KEY = "TU_LOCAL_KEY_16_CHARS"

# Puerto en el que escuchará este servidor local
PUERTO    = 8080


tira = tinytuya.OutletDevice(DEVICE_ID, IP_TIRA, LOCAL_KEY)
tira.set_version(3.3)

DP_SWITCH = "20"
DP_MODE   = "21"
DP_BRILLO = "22"
DP_COLOR  = "24"

COLORES = {"rojo": 0, "naranja": 30, "amarillo": 60, "verde": 120,
           "cian": 180, "azul": 240, "morado": 280, "rosa": 320}

def color_hex(h, s, v):
    return f"{h:04x}{s:04x}{v:04x}"

def rgb_a_tuya(hexrgb):
    hexrgb = hexrgb.lstrip("#")
    r, g, b = (int(hexrgb[i:i+2], 16) / 255 for i in (0, 2, 4))
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    return color_hex(round(h * 360), round(s * 1000), round(v * 1000))

class Traductor(BaseHTTPRequestHandler):
    def orden(self, dp, valor):
        r = tira.set_value(dp, valor)
        print("   el dispositivo responde:", r)
        if isinstance(r, dict) and ("Error" in r or "Err" in r):
            raise Exception(str(r))
        return r

    def responder(self, texto, codigo=200):
        self.send_response(codigo)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(texto.encode())

    def do_GET(self):
        p = [x for x in self.path.split("/") if x]
        print("Peticion recibida:", self.path)
        try:
            if p == ["luz", "on"]:
                self.orden(DP_SWITCH, True)
                return self.responder("Luz encendida")
            if p == ["luz", "off"]:
                self.orden(DP_SWITCH, False)
                return self.responder("Luz apagada")
            if p == ["luz", "estado"]:
                return self.responder(str(tira.status()))
            if p[:2] == ["luz", "brillo"] and len(p) == 3:
                pct = max(1, min(100, int(p[2])))
                self.orden(DP_SWITCH, True)
                self.orden(DP_MODE, "white")
                self.orden(DP_BRILLO, pct * 10)
                return self.responder(f"Brillo al {pct}%")
            if p[:2] == ["luz", "color"] and len(p) >= 3:
                nombre = p[2].lower()
                brillo = int(p[3]) * 10 if len(p) == 4 else 1000
                self.orden(DP_SWITCH, True)
                if nombre == "blanco":
                    self.orden(DP_MODE, "white")
                    return self.responder("Color: blanco")
                self.orden(DP_MODE, "colour")
                if nombre in COLORES:
                    self.orden(DP_COLOR, color_hex(COLORES[nombre], 1000, brillo))
                    return self.responder(f"Color: {nombre}")
                if len(nombre) == 6:
                    self.orden(DP_COLOR, rgb_a_tuya(nombre))
                    return self.responder(f"Color: #{nombre}")
                return self.responder("Color no reconocido", 400)
            return self.responder("Prueba: /luz/on /luz/off /luz/brillo/50 /luz/color/azul", 404)
        except Exception as e:
            return self.responder(f"Error: {e}", 500)

if __name__ == "__main__":
    print(f"LOCAL_KEY cargada con {len(LOCAL_KEY)} caracteres (deberian ser 16)")
    print(f"Traductor escuchando en el puerto {PUERTO}")
    HTTPServer(("0.0.0.0", PUERTO), Traductor).serve_forever()