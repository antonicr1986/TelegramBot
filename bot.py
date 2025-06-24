import asyncio
import os
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

preguntas_trivia = [
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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Limpia el estado anterior (como trivia activa)
    context.user_data["respuesta_correcta"] = None

    # Activa el bot
    context.application.bot_data["activo"] = True

    await update.message.reply_text(
        "🔓 Bot activado. ¡Hola! Soy tu bot hecho por Antonio Company.\n"
        "Usa /help para ver los comandos disponibles."
    )
    
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    limpiar_estado(context)
    if not context.application.bot_data.get("activo", True):
        await update.message.reply_text("🚫 El bot está inactivo. Usa /start para activarlo de nuevo.")
        return

    help_text = (
        "🤖 *Lista de comandos disponibles:*\n\n"
        "/start - Iniciar el bot\n"
        "/help - Mostrar esta ayuda\n"
        "/dado - Para lanzar un dado virtual\n"
        "/pregunta - Para probar tu sabiduria\n"
        "/recordar - Para poner activo un recordatorio en x minutos y con el mensaje deseado\n\n"
        "Escribe cualquier texto y te lo repetiré en mayúsculas con la cantidad de caracteres\n"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")

async def echo_util(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto_usuario = update.message.text
    texto_mayus = texto_usuario.upper()
    longitud = len(texto_usuario)
    respuesta = f"Tú escribiste:\n{texto_mayus}\n\nNúmero de caracteres: {longitud}"
    await update.message.reply_text(update.message.text)
    
async def lanzar_dado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    limpiar_estado(context)
    if not context.application.bot_data.get("activo", True):
        await update.message.reply_text("🚫 El bot está inactivo. Usa /start para activarlo de nuevo.")
        return

    numero = random.randint(1, 6)

    retos = {
        1: "😵 ¡Oh no! Sacaste un 1.\n*Reto:* Envía un emoji que te represente ahora mismo 😅",
        2: "🙃 Un 2... la suerte está tímida hoy.\n*Reto:* Escribe una frase usando solo palabras de 3 letras o menos 🤓",
        3: "😐 Un 3, estás a mitad de camino.\n*Reto:* Manda un chiste malo… pero que te haga reír igual 😄",
        4: "🙂 Un 4. Empieza a verse bien...\n*Reto:* Inventa un superpoder inútil y descríbelo 🦸‍♂️",
        5: "😄 Un 5. ¡Casi perfecto!\n*Reto:* Menciona una canción que siempre te anima 🎶",
        6: "🎉 ¡BOOM! Un 6, tirada legendaria.\n*Reto:* Escribe una frase como si fueras un supervillano declarando su plan 😈"
    }

    mensaje = f"🎲 El dado cayó en: *{numero}*\n\n{retos[numero]}"
    await update.message.reply_text(mensaje, parse_mode="Markdown")

async def enviar_pregunta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.application.bot_data.get("activo", True):
        await update.message.reply_text("🚫 El bot está inactivo. Usa /start para activarlo de nuevo.")
        return
    
    pregunta = random.choice(preguntas_trivia)
    texto = f"🧠 *Pregunta Trivia:*\n\n{pregunta['pregunta']}\n" + "\n".join(pregunta["opciones"])
    texto += "\n\n(Responde con A, B, C o D)"
    # Puedes guardar la respuesta correcta en el contexto si luego quieres validarla
    context.user_data["respuesta_correcta"] = pregunta["respuesta_correcta"]
    await update.message.reply_text(texto, parse_mode="Markdown")
    
async def verificar_respuesta(update: Update, context: ContextTypes.DEFAULT_TYPE):

    respuesta_esperada = context.user_data.get("respuesta_correcta")
    respuesta_usuario = update.message.text.strip().upper()

    if respuesta_esperada:
        if respuesta_usuario == respuesta_esperada:
            mensaje = "🎉 ¡Respuesta correcta! ¡Eres un crack del conocimiento!"
        elif respuesta_usuario in ["A", "B", "C", "D"]:
            mensaje = f"❌ Respuesta incorrecta. La opción correcta era *{respuesta_esperada}*."
        else:
            mensaje = "⚠️ Por favor, responde con A, B, C o D."
    else:
        mensaje = "ℹ️ No hay una pregunta activa. Usa /pregunta para recibir una."

    await update.message.reply_text(mensaje, parse_mode="Markdown")
    
async def cancelar_trivia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    limpiar_estado(context)

    context.user_data["respuesta_correcta"] = None
    await update.message.reply_text("🔕 Pregunta cancelada. Ya no espero respuesta. Usa /pregunta para otra.")
    
async def recordar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    limpiar_estado(context)
    if not context.application.bot_data.get("activo", True):
        await update.message.reply_text("🚫 El bot está inactivo. Usa /start para activarlo de nuevo.")
        return

    try:
        minutos = int(context.args[0])
        mensaje = " ".join(context.args[1:])
        if minutos <= 0 or not mensaje:
            raise ValueError
    except (IndexError, ValueError):
        await update.message.reply_text("⏳ Usa el comando así: `/recordar [minutos] [mensaje]`\nEjemplo: `/recordar 5 Tomar agua 💧`", parse_mode="Markdown")
        return

    await update.message.reply_text(f"🕒 ¡Te recordaré esto en {minutos} minuto(s)!")

    await asyncio.sleep(minutos * 60)  # Espera el tiempo indicado
    await update.message.reply_text(f"🔔 *Recordatorio:* {mensaje}", parse_mode="Markdown")

def limpiar_estado(context: ContextTypes.DEFAULT_TYPE):
    context.user_data["respuesta_correcta"] = None
    
async def parar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.application.bot_data["activo"] = False
    context.user_data["respuesta_correcta"] = None
    await update.message.reply_text("🔒 Bot desactivado. Usa /start para activarlo de nuevo.")


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("dado", lanzar_dado))
    app.add_handler(CommandHandler("pregunta", enviar_pregunta))
    app.add_handler(
    MessageHandler(
        filters.TEXT & (~filters.COMMAND),
        verificar_respuesta
    ),
    group=1  # ← lo ponemos en un grupo separado
)
    app.add_handler(CommandHandler("cancelar", cancelar_trivia))
    app.add_handler(CommandHandler("recordar", recordar))
    app.add_handler(CommandHandler("parar", parar))
    
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo_util))

    print("Bot corriendo... presiona Ctrl+C para detenerlo")
    app.run_polling()

if __name__ == "__main__":
    # Evita errores con event loops ya activos
    try:
        asyncio.run(main())
    except RuntimeError as e:
        if "event loop is already running" in str(e):
            print("El event loop ya está corriendo, ejecutando con otra estrategia.")
            loop = asyncio.get_event_loop()
            loop.create_task(main())
            loop.run_forever()
        else:
            raise