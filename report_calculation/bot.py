import logging
from typing import Optional

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, User
from telegram.constants import ParseMode
from telegram.ext import CallbackQueryHandler, CommandHandler, ContextTypes

from report_calculation.actions.calculate import (
    invested_euros,
    invested_usd,
    profit_euros,
    profit_usd,
    total_crypto_euros,
    total_crypto_usd,
    total_euros,
    total_usd,
)
from report_calculation.actions.currency import create, delete, read, update
from report_calculation.config import telegram_app
from report_calculation.errors import NotUserFound
from report_calculation.model import User as ModelUser

logger = logging.getLogger(__name__)


def _get_user(
    bot_info: User,
) -> Optional[ModelUser]:  # TODO add <class 'telegram._user.User'> typing
    users = ModelUser.find(telegram_id=str(bot_info.id))
    if users:
        return users[-1]
    return None


async def start(update_handler: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with three inline buttons attached."""
    logger.info(f"Launching keyboard buttons")
    keyboard = [
        [
            InlineKeyboardButton("total usd", callback_data="total_usd"),
            InlineKeyboardButton("total euros", callback_data="total_euros"),
        ],
        [
            InlineKeyboardButton("total crypto usd", callback_data="total_crypto_usd"),
            InlineKeyboardButton(
                "total crypto euros", callback_data="total_crypto_euros"
            ),
        ],
        [
            InlineKeyboardButton("profit usd", callback_data="profit_usd"),
            InlineKeyboardButton("profit euros", callback_data="profit_euros"),
        ],
        [
            InlineKeyboardButton("investment usd", callback_data="investment_usd"),
            InlineKeyboardButton("investment euros", callback_data="investment_euros"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update_handler.message.reply_text("Please choose:", reply_markup=reply_markup)


async def help_command(
    update_handler: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Displays info on how to use the bot."""
    logger.info(f"Launching help command")
    await update_handler.message.reply_text("Use /start to test this bot.")


# Total money on cryptos


async def get_total_crypto_usd(
    update_handler: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    logger.info(f"Running get_total_crypto_usd")
    await update_handler.callback_query.edit_message_text(
        "Calculating total crypto money in usd"
    )
    await update_handler.callback_query.message.reply_text(
        f"Total crypto money: {await total_crypto_usd(_get_user(await context.bot.get_me()))} usd"
    )


async def get_total_crypto_euros(
    update_handler: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    logger.info(f"Running get_total_crypto_euros")
    await update_handler.callback_query.edit_message_text(
        "Calculating total crypto money in euros"
    )
    await update_handler.callback_query.message.reply_text(
        f"Total crypto money: {await total_crypto_euros(_get_user(await context.bot.get_me()))} euros"
    )


# Total money (total money on cryptos + bank savings)


async def get_total_usd(
    update_handler: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    logger.info(f"Running get_total_usd")
    await update_handler.callback_query.edit_message_text(
        "Calculating total money in usd (total crypto money + bank savings)"
    )
    await update_handler.callback_query.message.reply_text(
        f"Total money: {await total_usd(_get_user(await context.bot.get_me()))} usd"
    )


async def get_total_euros(
    update_handler: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    logger.info(f"Running get_total_euros")
    await update_handler.callback_query.edit_message_text(
        "Calculating total money in euros (total crypto money + bank savings)"
    )
    await update_handler.callback_query.message.reply_text(
        f"Total money: {await total_euros(_get_user(await context.bot.get_me()))} euros"
    )


# Total profit (total money on cryptos - investment)


async def get_profit_usd(
    update_handler: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    logger.info(f"Running get_profit_usd")
    await update_handler.callback_query.edit_message_text(
        "Calculating total profit in usd (total crypto money - investment)"
    )
    await update_handler.callback_query.message.reply_text(
        f"Total profit: {await profit_usd(_get_user(await context.bot.get_me()))} usd"
    )


async def get_profit_euros(
    update_handler: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    logger.info(f"Running get_profit_euros")
    await update_handler.callback_query.edit_message_text(
        "Calculating total profit in euros (total crypto money - investment)"
    )
    await update_handler.callback_query.message.reply_text(
        f"Total profit: {await profit_euros(_get_user(await context.bot.get_me()))} euros"
    )


# Total invested money


async def get_investment_usd(
    update_handler: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    logger.info(f"Running get_investment_usd")
    await update_handler.callback_query.edit_message_text("Total invested money in usd")
    await update_handler.callback_query.message.reply_text(
        f"Total money: {await invested_usd(_get_user(await context.bot.get_me()))} usd"
    )


async def get_investment_euros(
    update_handler: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    logger.info(f"Running get_investment_euros")
    await update_handler.callback_query.edit_message_text(
        "Total invested money in euros"
    )
    await update_handler.callback_query.message.reply_text(
        f"Total money: {await invested_euros(_get_user(await context.bot.get_me()))} euros"
    )


## CRUD handlers
# add new crypto in database


async def create_currency(
    update_handler: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    logger.info(f"Running create_currency")

    user: ModelUser = _get_user(await context.bot.get_me())
    if not user:
        raise NotUserFound(message="Not user found")

    if context.args:
        await update_handler.message.reply_text(
            f"Adding {context.args[0]} with value {context.args[1]}"
        )
        await update_handler.message.reply_text(
            f"Added {create(user.user_id, context.args[0], context.args[1])}"
        )
    else:
        await update_handler.message.reply_text(
            f"Please introduce symbol and quantity as arguments"
        )


# get crypto data


async def read_currency(
    update_handler: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    logger.info(f"Running read_currency")

    user: ModelUser = _get_user(await context.bot.get_me())
    if not user:
        raise NotUserFound(message="Not user found")

    if context.args:
        symbol = context.args[0]
        await update_handler.message.reply_text(f"Reading {symbol} data")
        await update_handler.message.reply_text(f"Result {read(user.user_id, symbol)}")
    else:
        await update_handler.message.reply_text(f"Reading all data")
        currencies = read(user.user_id)
        message = "Result: \n"
        for currency in currencies:  # type: ignore
            message += f"* <b>{currency.symbol} :</b> {currency.quantity} \n"
        await update_handler.message.reply_text(message, parse_mode=ParseMode.HTML)


# update crypto data


async def update_currency(
    update_handler: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    logger.info(f"Running update_currency")

    user: ModelUser = _get_user(await context.bot.get_me())
    if not user:
        raise NotUserFound(message="Not user found")

    if context.args:
        await update_handler.message.reply_text(
            f"Updating {context.args[0]} with value {context.args[1]}"
        )
        await update_handler.message.reply_text(
            f"Updated {update(user.user_id, context.args[0], context.args[1])}"
        )
    else:
        await update_handler.message.reply_text(
            f"Please introduce symbol and quantity as arguments"
        )


# delete existing from db


async def delete_currency(
    update_handler: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    logger.info(f"Running delete_currency")

    user: ModelUser = _get_user(await context.bot.get_me())
    if not user:
        raise NotUserFound(message="Not user found")

    if context.args:
        await update_handler.message.reply_text(f"Deleting {context.args[0]} data")
        await update_handler.message.reply_text(
            f"Deleted {delete(user.user_id, context.args[0])}"
        )
    else:
        await update_handler.message.reply_text(f"Please introduce symbol as arguments")


# Error handlers


async def error_handler(
    update_handler: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Log the error and send a telegram message to notify the client."""
    logger.error("Error %s", context.error)
    message = (
        f"An exception was raised while handling a command\n"
        f"<pre>{context.error}</pre>"
    )
    await update_handler.message.reply_text(
        message, parse_mode=ParseMode.HTML
    )  # TODO To fix, it is not working


# get bot_info


async def bot_info(update_handler: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"Geting bot information")
    await update_handler.message.reply_text(
        f"bot information {await context.bot.get_me()}"
    )


telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(
    CallbackQueryHandler(get_total_crypto_usd, pattern="total_crypto_usd")
)
telegram_app.add_handler(
    CallbackQueryHandler(get_total_crypto_euros, pattern="total_crypto_euros")
)
telegram_app.add_handler(CallbackQueryHandler(get_total_usd, pattern="total_usd"))
telegram_app.add_handler(CallbackQueryHandler(get_total_euros, pattern="total_euros"))
telegram_app.add_handler(CallbackQueryHandler(get_profit_usd, pattern="profit_usd"))
telegram_app.add_handler(CallbackQueryHandler(get_profit_euros, pattern="profit_euros"))
telegram_app.add_handler(
    CallbackQueryHandler(get_investment_usd, pattern="investment_usd")
)
telegram_app.add_handler(
    CallbackQueryHandler(get_investment_euros, pattern="investment_euros")
)
telegram_app.add_handler(CommandHandler("help", help_command))
telegram_app.add_handler(CommandHandler("update", update_currency))
telegram_app.add_handler(CommandHandler("get", read_currency))
telegram_app.add_handler(CommandHandler("add", create_currency))
telegram_app.add_handler(CommandHandler("delete", delete_currency))
telegram_app.add_handler(CommandHandler("bot", bot_info))
telegram_app.add_error_handler(error_handler)
