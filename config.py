import os

# Token del bot (usa variables de entorno para mayor seguridad)
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Preguntas de trivia: puedes ampliarlo o cargarlo desde un archivo externo si quieres
PREGUNTAS_TRIVIA = [
    {
        "pregunta": "¿Cuál es el planeta más grande del sistema solar?",
        "opciones": ["A) Marte", "B) Júpiter", "C) Saturno", "D) Tierra"],
        "respuesta_correcta": "B"
    },
    {
        "pregunta": "¿Quién pintó la Mona Lisa?",
        "opciones": ["A) Miguel Ángel", "B) Van Gogh", "C) Da Vinci", "D) Picasso"],
        "respuesta_correcta": "C"
    },
    {
        "pregunta": "¿Cuántos lados tiene un hexágono?",
        "opciones": ["A) 5", "B) 6", "C) 7", "D) 8"],
        "respuesta_correcta": "B"
    }
]

HELP_TEXT = (
    "🤖 *Lista de comandos disponibles:*\n\n"
    "/start - Iniciar el bot\n"
    "/help - Mostrar esta ayuda\n"
    "/dado - Para lanzar un dado virtual\n"
    "/pregunta - Para probar tu sabiduría\n"
    "/recordar - Activar un recordatorio en x minutos\n"
    "/stop - Para poner inactivo el estado del bot\n\n"
    "Escribe cualquier texto y te lo repetiré en mayúsculas con la cantidad de caracteres\n"
)