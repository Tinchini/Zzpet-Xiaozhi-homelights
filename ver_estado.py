import tinytuya, json

# --- CONFIGURACIÓN DE TU DISPOSITIVO TUYA ---
# Reemplaza estos valores por los datos de tu dispositivo Tuya:
DEVICE_ID = "TU_DEVICE_ID_AQUI"
IP_TIRA   = "TU_IP_LOCAL_DE_LA_TIRA"
LOCAL_KEY = "TU_LOCAL_KEY_16_CHARS"


d = tinytuya.OutletDevice(DEVICE_ID, IP_TIRA, LOCAL_KEY)
d.set_version(3.3)

estado = d.status()
print(json.dumps(estado, indent=2, ensure_ascii=False))