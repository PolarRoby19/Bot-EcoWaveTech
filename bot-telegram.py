#pip install python-telegram-bot
#pip install python-telegram-bot --upgrade

from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN: Final = '8006774425:AAHdbzhelzOgnB7IiUxfvmlfj2R6d0rbhFk'
BOT_USERNAME: Final = '@EcoWaveTech_bot'

# command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'Ciao {update.effective_user.first_name}!!👋 \nProva l intelligenza artificiale di EcoWaveTech🐟.\nPer sapere come funzione digita il comando /help')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Carica un immagine del pesce di cui vuoi sapere la famiglia")

# text response
def handle_response(text: str) -> str:
    processed: str = text.lower()

    if 'ciao' in processed:
        return 'Buongiorno👋 se vuoi sapere come funziono scrivi "\help"'

    if 'arrivederci' in processed:
        return 'Buonagiornata 👋'

    return 'Non capisco'

# error
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} ha causato un errore {context.error}')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'Utente ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text : str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
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