
import pymongo


from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext,
     MessageHandler,
    filters
)

from config import *

mom = pymongo.MongoClient(MONGO_DB_URL)
db = mom['USERS']
collection = db['users']

async def start(update: Update, context: CallbackContext) -> None:

    user_id = update.message.from_user.id

    if collection.find_one({'user_id': user_id}) is None:

        collection.insert_one({'user_id': user_id})

    await update.message.reply_text('Hello!')

async def post(update: Update, context: CallbackContext) -> None:

    user_id = update.message.from_user.id

    if user_id != ADMIN_ID:

        await update.message.reply_text('You are not admin!')

        return

    msg_id = update.message.reply_to_message.message_id

    if msg_id is None:

        await update.message.reply_text('Reply to a message to post it!')

        return
    
    text = f'Total users: {str(collection.count_documents({}))}\n\nSucess: 0'

    msg = await update.message.reply_text(text)

    po = 0
   
    for user in collection.find():

        try:

            await context.bot.copy_message(chat_id=user['user_id'], from_chat_id=update.message.chat_id, message_id=msg_id)

            po += 1

            text = f'Total users: {str(collection.count_documents({}))}\n\nSucess: {str(po)}'

            await msg.edit_text(text)

        except:

            pass

    
    try:

        await context.bot.copy_message(chat_id=GROUP_ID, from_chat_id=update.message.chat_id, message_id=msg_id)

        await update.message.reply_text('sent to group')

    except:

        pass

    

def main():

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    
    app.add_handler(CommandHandler('post', post))

    print("Bot started")

    app.run_polling()

   

if __name__ == '__main__':

    main()





