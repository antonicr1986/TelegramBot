import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola! Soy tu bot. Usa /help para ver los comandos.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🤖 *Lista de comandos disponibles:*\n\n"
        "/start - Iniciar el bot\n"
        "/help - Mostrar esta ayuda\n"
        "Escribe cualquier texto y te lo repetiré en mayúsculas con la cantidad de caracteres\n"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")

async def echo_util(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto_usuario = update.message.text
    texto_mayus = texto_usuario.upper()
    longitud = len(texto_usuario)
    respuesta = f"Tú escribiste:\n{texto_mayus}\n\nNúmero de caracteres: {longitud}"
    await update.message.reply_text(update.message.text)

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
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