import asyncio
import logging
import sys
from config import settings

from aiogram import Bot, Dispatcher, Router, types, filters
from aiogram.enums import ParseMode
from aiogram.utils import markdown


# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()


@dp.message(filters.CommandStart())
async def command_start_handler(message: types.Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(f"Hello, {markdown.hbold(message.from_user.full_name)}!")


@dp.message()
async def echo_handler(message: types.Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        # Send a copy of the received message
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")


def main():
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(settings.TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching

    # await dp.start_polling(bot)
    dp.run_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    main()
