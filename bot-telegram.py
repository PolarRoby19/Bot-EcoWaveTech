import os
from typing import Final
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Carica le variabili d'ambiente dal file .env
load_dotenv()

# Ottieni il token e il nome utente del bot dalle variabili d'ambiente
TOKEN: Final = os.getenv('TELEGRAM_BOT_TOKEN')
BOT_USERNAME: Final = os.getenv('BOT_USERNAME')

# Verifica se il token è stato caricato correttamente
if TOKEN is None:
    print("Errore: La variabile d'ambiente TELEGRAM_BOT_TOKEN non è stata trovata")
    exit()

# Verifica se il nome utente del bot è stato caricato correttamente
if BOT_USERNAME is None:
    print("Errore: La variabile d'ambiente BOT_USERNAME non è stata trovata")
    exit()

# command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'Ciao {update.effective_user.first_name}!!👋 \nProva l intelligenza artificiale di EcoWaveTech🐟.\nPer sapere come funzione digita il comando /help')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Carica un immagine del pesce di cui vuoi sapere la famiglia")

# Funzione per inviare una foto a un utente specifico tramite il suo ID
async def send_photo_to_user(context: ContextTypes.DEFAULT_TYPE, user_id: int, photo_path: str = None, photo_bytes: bytes = None, caption: str = None):
    try:
        if photo_path:
            await context.bot.send_photo(chat_id=user_id, photo=photo_path, caption=caption)
            print(f"Foto inviata all'utente {user_id} dal percorso: {photo_path}")
        elif photo_bytes:
            await context.bot.send_photo(chat_id=user_id, photo=photo_bytes, caption=caption)
            print(f"Foto inviata all'utente {user_id} dai bytes.")
        else:
            print(f"Errore: Nessun percorso o bytes forniti per l'invio della foto all'utente {user_id}.")
    except Exception as e:
        print(f"Errore nell'invio della foto all'utente {user_id}: {e}")

specific_user_id_str: str | None = os.getenv("SPECIFIC_USER_ID")
SPECIFIC_USER_ID: Final = int(specific_user_id_str) if specific_user_id_str else None
IMAGE_TO_SEND_PATH: Final = os.getenv("IMAGE_TO_SEND_PATH")
IMAGE_CAPTION: Final = os.getenv("IMAGE_CAPTION")

# text response
def handle_response(text: str) -> str:
    processed: str = text.lower()

    if 'ciao' in processed:
        return 'Buongiorno👋 se vuoi sapere come funziono scrivi "/help"'

    if 'arrivederci' in processed:
        return 'Buonagiornata 👋'

    return 'Non capisco'

# error
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} ha causato un errore {context.error}')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    user_id = update.message.chat.id
    text: str = update.message.text

    print(f'Utente ({user_id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text : str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    elif message_type == 'private':
        if user_id == SPECIFIC_USER_ID and 'ciao' in text.lower():
            await send_photo_to_user(context, user_id, photo_path=IMAGE_TO_SEND_PATH, caption=IMAGE_CAPTION)
        elif user_id != SPECIFIC_USER_ID and 'ciao' in text.lower():
            response: str = handle_response(text)
            print('Bot:', response)
            await update.message.reply_text(response)
        else:
            response: str = handle_response(text)
            print('Bot:', response)
            await update.message.reply_text(response)

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    photo = update.message.photo[-1]
    await context.bot.send_photo(chat_id=chat_id, photo=photo.file_id, caption="Ecco la tua immagine!")

print('Avvio del Bot....')
app = Application.builder().token(TOKEN).build()

# Commands
app.add_handler(CommandHandler('start', start_command))
app.add_handler(CommandHandler('help', help_command))

# Messages
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Images
app.add_handler(MessageHandler(filters.PHOTO, handle_image))

# Error
app.add_error_handler(error)

app.run_polling(poll_interval=1)