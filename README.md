# 🐾 ZzPet - Control de Luces LED Inteligentes (Tuya / Smart Life + Xiaozhi AI)

Controla tu tira de luces LED inteligente por voz o mediante Inteligencia Artificial usando **Xiaozhi AI / ZzPet** y el protocolo **MCP (Model Context Protocol)**, comunicándote directamente de forma local con dispositivos compatibles con el ecosistema **Tuya / Smart Life**.

---

## 🌟 ¿Qué hace este proyecto?

Este proyecto te permite conectar tu mascota o asistente de IA (**Xiaozhi / ZzPet**) con las luces LED de tu habitación o escritorio:

- 🗣️ **Comandos de voz naturales**: Pídele a la IA *"enciende la luz"*, *"pon la luz en color azul"*, *"baja el brillo al 30%"*, etc.
- ⚡ **Control Local Ultra-rápido**: Una vez configurado, las órdenes a la luz se envían directamente por tu red WiFi local (a través de la librería `tinytuya`), sin depender de la nube lenta de Tuya.
- 🔌 **Integración MCP**: Implementa un servidor MCP estándar que expone herramientas (`encender_luz`, `apagar_luz`, `cambiar_color`, `cambiar_brillo`, `obtener_estado_luz`) para que el agente de IA las use automáticamente cuando tú se lo pidas.

---

## 🧱 Arquitectura del Proyecto (¿Cómo funciona por dentro?)

```
[ Usuario / Voz ]
       │
       ▼
[ Xiaozhi / ZzPet AI ]
       │ (WebSocket seguro MCP)
       ▼
[ mcp-calculator / mcp_pipe.py + luz_mcp.py ]  <-- Servidor de Herramientas MCP
       │ (HTTP Local en puerto 8080)
       ▼
[ traductor.py ]  <-- Servidor Traductor Local
       │ (Protocolo Local Tuya 3.3 vía WiFi)
       ▼
[ Tira LED Inteligente Tuya ]
```

---

## 📋 Requisitos Previos

1. **Una tira LED o bombilla compatible con Tuya / Smart Life**.
2. **Un ordenador con Windows** (conectado a la misma red WiFi que la tira LED).
3. **Python 3.10 o superior** instalado en tu PC ([Descargar Python](https://www.python.org/downloads/) - *marca la casilla "Add python.exe to PATH"*).
4. Un dispositivo o cliente con **Xiaozhi AI** configurado con tu token MCP.

---

## 🔑 GUÍA PASO A PASO: Cómo obtener los datos de tu tira LED

Para que tu PC pueda controlar la tira LED sin pasar por internet, necesitas 3 datos:
1. **Device ID** (Identificador del dispositivo).
2. **Local Key** (Clave secreta de 16 caracteres para cifrar la comunicación).
3. **Dirección IP local** de la tira en tu router (ejemplo: `192.168.1.50`).

Sigue estos sencillos pasos:

### Paso 1: Configurar la app en tu teléfono
1. Descarga la aplicación **Smart Life** o **Tuya Smart** en tu teléfono móvil (desde Google Play Store o Apple App Store).
2. Vincula tu tira LED a la app y asegúrate de que puedes encenderla y cambiarle el color desde tu teléfono.

### Paso 2: Crear cuenta en la plataforma de desarrolladores de Tuya (Es gratis)
1. Entra en [Tuya IoT Platform](https://iot.tuya.com/) y crea una cuenta gratuita.
2. Inicia sesión y ve a **Cloud** (Nube) -> **Development** (Desarrollo) -> **Create Cloud Project** (Crear proyecto en la nube).
3. Ponle un nombre a tu proyecto (ej: `MiCasa`) y selecciona tu región (ej: Europa Occidental o América).
4. En la pestaña **Devices** (Dispositivos) -> **Link Tuya App Account** (Vincular cuenta de la App Tuya):
   - Te saldrá un código QR en la pantalla del ordenador.
   - Abre la app **Smart Life / Tuya** en tu teléfono, ve a **Perfil** -> toca el icono de **Escanear QR** en la esquina superior y escanea el código del ordenador.
   - ¡Listo! Tu teléfono y tus dispositivos ya están vinculados a tu cuenta de desarrollador.
5. Ve a la pestaña **Overview** (Vista general) de tu proyecto en la web y copia:
   - **Access ID / Client ID**
   - **Access Secret / Client Secret**

### Paso 3: Obtener la Local Key automáticamente usando TinyTuya
En tu ordenador, abre la consola (CMD o PowerShell) y escribe:

```bash
python -m tinytuya wizard
```

El asistente te hará 3 preguntas sencillas:
1. Pega tu **API Key** (Access ID).
2. Pega tu **API Secret**.
3. Selecciona tu región (ej: `eu` para Europa o `us` para América).

Al terminar, TinyTuya escaneará tu red WiFi y generará un archivo llamado `devices.json`. Ábrelo con el bloc de notas y verás:
- `"id"`: Tu **Device ID**
- `"key"`: Tu **Local Key** (clave de 16 caracteres)
- `"ip"`: La **IP de la tira** en tu red local.

---

## ⚙️ Configuración del Proyecto

### 1. Clonar o descargar este repositorio
Descarga este proyecto en una carpeta de tu ordenador.

### 2. Instalar las dependencias
Abre una consola en la carpeta del proyecto y ejecuta:
```bash
pip install -r requirements.txt
```

### 3. Poner tus datos en `traductor.py`
Abre el archivo `traductor.py` con cualquier editor de texto o Bloc de notas y rellena tus datos en las primeras líneas:

```python
DEVICE_ID = "PEGA_AQUI_TU_DEVICE_ID"
IP_TIRA   = "PEGA_AQUI_LA_IP_DE_TU_TIRA"  # Ej: "192.168.1.50"
LOCAL_KEY = "PEGA_AQUI_TU_LOCAL_KEY"     # Clave de 16 caracteres
PUERTO    = 8080
```

*(Opcional: Si quieres probar primero que la comunicación funciona, pon los mismos datos en `prueba_mando.py` y ejecútalo con `python prueba_mando.py`)*.

### 4. Configurar tu Endpoint de Xiaozhi
1. Entra en la carpeta `mcp-calculator`.
2. Haz una copia del archivo `.env.example` y renómbralo exactamente a `.env`.
3. Ábrelo y pega el enlace del endpoint que te dio Xiaozhi:
   ```env
   MCP_ENDPOINT=wss://api.xiaozhi.me/mcp/?token=TU_TOKEN_AQUI
   ```

---

## 🚀 Cómo ponerlo en marcha

Para iniciar todo a la vez con un solo clic:

1. Haz **doble clic en `ZzPet_luces.bat`**.
2. Se abrirán dos ventanas automáticamente:
   - **ZzPet Luces - Traductor**: Servidor local que traduce las peticiones a órdenes Tuya.
   - **ZzPet Luces - MCP Pipe**: Conector WebSocket que enlaza con Xiaozhi.
3. ¡Ya está funcionando! Ahora puedes hablarle a tu Xiaozhi / ZzPet y pedirle que controle las luces.

---

## 🛠️ Herramientas MCP disponibles

El asistente de Inteligencia Artificial tiene a su disposición las siguientes funciones automáticas:

| Herramienta | Descripción | Parámetros |
| :--- | :--- | :--- |
| `encender_luz()` | Enciende la tira LED. | Ninguno |
| `apagar_luz()` | Apaga la tira LED. | Ninguno |
| `cambiar_color(color, brillo)` | Cambia el color (rojo, verde, azul, amarillo, etc., o código Hex `#FF0000`). | `color` (texto), `brillo` (1-100 opcional) |
| `cambiar_brillo(porcentaje)` | Ajusta la intensidad de la luz manteniendo el color actual. | `porcentaje` (1-100) |
| `obtener_estado_luz()` | Consulta si la luz está encendida, qué color y qué brillo tiene. | Ninguno |

---

## ❓ Preguntas Frecuentes y Solución de Problemas

- **¿Por qué me da error de conexión a la IP de la tira?**  
  Asegúrate de que el ordenador y la tira LED estén conectados a la **misma red WiFi** (las tiras Tuya funcionan normalmente en redes de 2.4 GHz).
- **La IP de la tira cambia si reinicio el router:**  
  Es muy recomendable entrar a la configuración de tu router y asignarle una **IP fija / estática** a la tira LED para que nunca cambie.

---

## 📄 Licencia
Distribuido bajo la Licencia MIT. ¡Siéntete libre de modificarlo, mejorarlo y compartirlo con la comunidad!

## Creación mediante IA, by Me