from telegram.ext import ContextTypes

def limpiar_estado(context: ContextTypes.DEFAULT_TYPE):
    """
    Reinicia cualquier dato temporal del usuario, como respuestas pendientes de trivia.
    """
    context.user_data["respuesta_correcta"] = None