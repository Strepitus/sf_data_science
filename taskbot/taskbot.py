#!/usr/bin/env python3

import logging
import asyncio
from telegram import Update, ForceReply
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Define the admin user ID
ADMIN_USER_ID = 5949891017

# Store a mapping of message IDs to user IDs
message_user_map = {}

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf'Hello {user.mention_html()} , leave message and it will be redirected, files better pack in zip before send',
        reply_markup=ForceReply(selective=True),
    )

async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle messages from users and forward them to the admin."""
    user = update.message.from_user
    user_message = update.message.text if update.message.text else ""
    username = f'@{user.username}' if user.username else user.full_name
    forwarded_message = f"New task {username}:\n{user_message}"

    sent_message = None
    if update.message.text:
        sent_message = await context.bot.send_message(chat_id=ADMIN_USER_ID, text=forwarded_message)
    elif update.message.photo:
        photo = update.message.photo[-1].file_id
        caption = update.message.caption if update.message.caption else ""
        sent_message = await context.bot.send_photo(chat_id=ADMIN_USER_ID, photo=photo, caption=f"{forwarded_message}\n{caption}")
    elif update.message.video:
        video = update.message.video.file_id
        caption = update.message.caption if update.message.caption else ""
        sent_message = await context.bot.send_video(chat_id=ADMIN_USER_ID, video=video, caption=f"{forwarded_message}\n{caption}")
    elif update.message.audio:
        audio = update.message.audio.file_id
        sent_message = await context.bot.send_audio(chat_id=ADMIN_USER_ID, audio=audio, caption=forwarded_message)
    elif update.message.document:
        document = update.message.document.file_id
        sent_message = await context.bot.send_document(chat_id=ADMIN_USER_ID, document=document, caption=forwarded_message)

    if sent_message:
        message_user_map[sent_message.message_id] = user.id

async def handle_admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle replies from the admin and forward them to the original user."""
    if update.message.reply_to_message and update.message.reply_to_message.message_id in message_user_map:
        original_sender_id = message_user_map[update.message.reply_to_message.message_id]
        reply_message = update.message.text if update.message.text else ""

        if update.message.text:
            await context.bot.send_message(chat_id=original_sender_id, text=f"Reply from admin: {reply_message}")
        elif update.message.photo:
            photo = update.message.photo[-1].file_id
            await context.bot.send_photo(chat_id=original_sender_id, photo=photo, caption=f"Reply from admin:\n{reply_message}")
        elif update.message.video:
            video = update.message.video.file_id
            await context.bot.send_video(chat_id=original_sender_id, video=video, caption=f"Reply from admin:\n{reply_message}")
        elif update.message.audio:
            audio = update.message.audio.file_id
            await context.bot.send_audio(chat_id=original_sender_id, audio=audio, caption=f"Reply from admin:\n{reply_message}")
        elif update.message.document:
            document = update.message.document.file_id
            await context.bot.send_document(chat_id=original_sender_id, document=document, caption=f"Reply from admin:\n{reply_message}")

async def run_bot(application):
    """Run the bot."""
    logger.info("Initializing application...")
    await application.initialize()

    logger.info("Starting application...")
    await application.start()

    logger.info("Starting updater polling...")
    await application.updater.start_polling()

    logger.info("Updater polling started.")
    while True:
        await asyncio.sleep(1)

    logger.info("Stopping application...")
    await application.stop()

    logger.info("Shutting down application...")
    await application.shutdown()

def main():
    """Main entry point for the script."""
    # Create the Application and pass it your bot's token
    application = Application.builder().token("7412336887:AAErRZKndzO-zgk7smR3OY36LCJbWtglD3I").build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.ALL & ~filters.REPLY, handle_user_message))
    application.add_handler(MessageHandler(filters.REPLY, handle_admin_reply))

    # Run the bot
    asyncio.run(run_bot(application))

if __name__ == '__main__':
    main()
