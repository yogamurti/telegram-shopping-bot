import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from collections import defaultdict
from dotenv import load_dotenv

# Import environmental variables
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_KEY")

# Dictionary to store shopping lists for each user
shopping_lists = defaultdict(list)


# Add item to the shopping list
async def add_item(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    item = " ".join(context.args)

    if item:
        shopping_lists[user_id].append(item)
        await update.message.reply_text(f'Added "{item}" to your shopping list.')
    else:
        await update.message.reply_text(
            "Please specify an item to add. Example: /add milk"
        )


# View the shopping list
async def view_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    items = shopping_lists[user_id]

    if items:
        list_text = "\n".join(f"- {item}" for item in items)
        await update.message.reply_text(f"Your shopping list:\n{list_text}")
    else:
        await update.message.reply_text("Your shopping list is empty.")


# Remove an item from the shopping list
async def remove_item(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    item = " ".join(context.args)

    if item in shopping_lists[user_id]:
        shopping_lists[user_id].remove(item)
        await update.message.reply_text(f'Removed "{item}" from your shopping list.')
    else:
        await update.message.reply_text(
            f'Item "{item}" not found in your shopping list.'
        )


# Clear the shopping list
async def clear_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    shopping_lists[user_id].clear()
    await update.message.reply_text("Your shopping list has been cleared.")


# Main function to set up the bot
def main():
    # Create an Application instance
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("add", add_item))
    application.add_handler(CommandHandler("list", view_list))
    application.add_handler(CommandHandler("remove", remove_item))
    application.add_handler(CommandHandler("clear", clear_list))

    # Start the bot
    application.run_polling()


if __name__ == "__main__":
    main()
