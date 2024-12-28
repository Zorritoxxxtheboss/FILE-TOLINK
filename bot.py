import os
import logging
from flask import Flask, send_from_directory
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Configuración del bot
TOKEN = '7798610149:AAHhcv-uAwFl5koEBslmHSk_XSQ2nw711VE'
DOWNLOAD_FOLDER = 'download'
BASE_URL = 'http://localhost:5000/download/'  # Cambia esto si usas un servidor público

# Configuración del servidor Flask
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = DOWNLOAD_FOLDER

# Crear la carpeta de descarga si no existe
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Configuración del logging
logging.basicConfig(level=logging.INFO)

# Función para manejar el comando /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('¡Hola! Envíame cualquier archivo y lo descargaré para ti.')

# Función para manejar los archivos
def handle_files(update: Update, context: CallbackContext) -> None:
    file = update.message.document or update.message.photo[-1] if update.message.photo else None
    if file:
        file_id = file.file_id
        file_name = file.file_name if update.message.document else f"{file_id}.jpg"
        new_file = context.bot.get_file(file_id)
        file_path = os.path.join(DOWNLOAD_FOLDER, file_name)
        new_file.download(file_path)
        download_link = f"{BASE_URL}{file_name}"
        update.message.reply_text(f"Archivo descargado: {download_link}")
    else:
        update.message.reply_text("No se ha encontrado ningún archivo.")

# Rutas para servir los archivos
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Configuración del bot
def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.document | Filters.photo, handle_files))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    # Ejecutar el servidor Flask en segundo plano
    from threading import Thread
    flask_thread = Thread(target=app.run, kwargs={'port': 5000})
    flask_thread.start()
    
    # Ejecutar el bot de Telegram
    main()
