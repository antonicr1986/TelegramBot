import asyncio
from telegram.ext import ApplicationBuilder
from config import TOKEN
from handlers import cargar_handlers

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Cargar comandos y funciones
    cargar_handlers(app)

    print("🤖 Bot corriendo... presiona Ctrl+C para detenerlo")
    app.run_polling()

if __name__ == "__main__":
    main()
