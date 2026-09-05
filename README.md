# 🤖 Bot de Telegram

Bot de Telegram escrito en Python con
[python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot).
Proyecto de practica: trivia, dados, recordatorios y eco de mensajes.

## 💬 Comandos

| Comando | Que hace |
|---|---|
| `/start` | Activa el bot |
| `/help` | Muestra la lista de comandos |
| `/dado` | Lanza un dado virtual |
| `/pregunta` | Envia una pregunta de trivia con cuatro opciones |
| `/cancelar` | Cancela la pregunta en curso |
| `/recordar [minutos] [mensaje]` | Avisa pasados esos minutos. Ej: `/recordar 5 Tomar agua` |
| `/stop` | Deja el bot inactivo hasta el siguiente `/start` |

Cualquier texto que no sea un comando se responde en mayusculas junto con su
numero de caracteres. Si hay una pregunta de trivia abierta, el texto se toma
como respuesta.

## ⚙️ Puesta en marcha

**1. Crea el bot y consigue su token.** En Telegram, habla con
[@BotFather](https://t.me/BotFather), usa `/newbot` y guarda el token que te da.

**2. Instala las dependencias:**

    pip install -r requirements.txt

**3. Define el token como variable de entorno.**

En Windows (PowerShell), de forma permanente:

    setx TELEGRAM_BOT_TOKEN "el-token-que-te-dio-BotFather"

En Linux o macOS:

    export TELEGRAM_BOT_TOKEN="el-token-que-te-dio-BotFather"

**4. Arranca el bot:**

    python main.py

## 🔑 Sobre el token

El token **no esta en el repositorio y no debe estarlo**: quien lo tenga controla
el bot por completo. El codigo lo lee de la variable de entorno:

```python
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
```

Si prefieres un fichero `.env` en lugar de una variable de entorno, `.env` ya
esta en el `.gitignore`, pero hay que añadir `load_dotenv()` al principio de
`config.py` para que se lea. Tal como esta ahora, el codigo solo mira la
variable de entorno.

Este repositorio tiene ademas escaneo automatico de secretos con **gitleaks**
en cada push, que revisa todo el historial.

## 🗂️ Estructura

| Fichero | Contenido |
|---|---|
| `main.py` | Punto de entrada: arranca el bot y carga los comandos |
| `handlers.py` | La logica de cada comando |
| `config.py` | Token, preguntas de trivia y texto de ayuda |
| `utils.py` | Utilidades compartidas |
| `bot.py` | Version antigua, con todo en un solo fichero. No la usa nadie |

## 🛠️ Tecnologias

- Python 3.10
- python-telegram-bot 20.7

## ✍️ Autor

Antonio Company — [GitHub](https://github.com/antonicr1986) ·
[LinkedIn](https://www.linkedin.com/in/antoniocompany/)
