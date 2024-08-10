#!/usr/bin/env python3

import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Constants
ADMIN_USER_ID = 5949891017

# Global dictionary to map messages to users
message_user_map = {}

# Logging configuration
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Start command handler
async def start(update: Update, context):
    await update.message.reply_text("Hello! This bot will forward your messages to the admin.")

# Message handler to forward messages to admin
async def forward_to_admin(update: Update, context):
    user_id = update.message.from_user.id
    message_id = update.message.message_id

    # Forward the message to the admin
    forwarded_message = await context.bot.forward_message(
        chat_id=ADMIN_USER_ID, from_chat_id=user_id, message_id=message_id
    )

    # Map the forwarded message ID to the original user ID
    message_user_map[forwarded_message.message_id] = user_id

# Message handler to handle replies from admin
async def handle_admin_reply(update: Update, context):
    admin_id = update.message.from_user.id
    reply_to_message = update.message.reply_to_message

    if admin_id == ADMIN_USER_ID and reply_to_message:
        original_user_id = message_user_map.get(reply_to_message.message_id)
        if original_user_id:
            await context.bot.send_message(
                chat_id=original_user_id, text=update.message.text
            )

async def main():
    # Create the Application and pass it your bot's token
    application = Application.builder().token("7412336887:AAErRZKndzO-zgk7smR3OY36LCJbWtglD3I").build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_to_admin))
    application.add_handler(MessageHandler(filters.TEXT & filters.COMMAND, handle_admin_reply))

    # Run the bot until you press Ctrl-C
    await application.run_polling()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped.")
