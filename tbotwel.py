import config
import logging
import filters
import asyncio
import json
import string

from aiogram import Bot, Dispatcher, executor, types

from filters import IsAdminFilter

from aiogram.types import ContentType, Message, nlineKeyboardMarkup, InlineKeyboardButton

from aiogram.dispatcher import filters

from aiogram.dispatcher.filters import CommandStart

# Log level
logging.basicConfig(level=logging.INFO)

# Bot init
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

chat_id = config.GROUP_ID
owner_id = config.OWNER_ID

# Button url
urlkb = InlineKeyboardMarkup(row_width=1)
urlButton = InlineKeyboardButton(text='Your link 📬', url='https://')
urlButton2 = InlineKeyboardButton(text='Your link 📲', url='https://')
urlButton3 = InlineKeyboardButton(text='Your link ⚡️', url='https://')
urlkb.add(urlButton, urlButton2, urlButton3)


# Welcome new users
@dp.message_handler(content_types=["new_chat_members"], chat_id=config.GROUP_ID)
async def on_users_joined(message: types.Message):
    new_member = message.new_chat_members[0]
    message_bot = await message.answer(
        f"Welcome, *{new_member.mention}*✌️!\nThis is the best *community* chat🏝. Use the *links* 📲.",
        reply_markup=urlkb, parse_mode="Markdown"
    )
    await message.bot.delete_message(config.GROUP_ID, message.message_id)
    await asyncio.sleep(10800)  # Message deletion timer == seconds
    await message_bot.delete()


# Command start bot
@dp.message_handler(filters.CommandStart(), chat_id=config.GROUP_ID)
async def command_start_handler(message: types.Message):
    message_bot = await message.answer(
        f"*Hello {message.from_user.full_name}*🙂!",
        "\nThat's all - I'm limited to lines of code 👨‍💻!\nUse the commands: /i, /help.",
        parse_mode="Markdown"
    )
    await message.bot.delete_message(config.GROUP_ID, message.message_id)
    await asyncio.sleep(3600)  # Message deletion timer == seconds
    await message_bot.delete()


# Activate filters
dp.filters_factory.bind(IsAdminFilter)  # filters.py


# Ban command (admins only!)
@dp.message_handler(is_admin=True, commands=["ban"], commands_prefix="!/", chat_id=config.GROUP_ID)
async def cmd_ban(message: types.Message):
    if not message.reply_to_message:
        message_bot = await message.reply("Ban function - active.\nJustice will be served!⚖️")
        await asyncio.sleep(3600)  # Message deletion timer == seconds
        await message.bot.delete_message(config.GROUP_ID, message.message_id)
        await message_bot.delete()
        return

    await message.bot.delete_message(config.GROUP_ID, message.message_id)
    await message.bot.kick_chat_member(chat_id=config.GROUP_ID, user_id=message.reply_to_message.from_user.id)
    message_bot = await message.reply_to_message.reply(
        f"Chat member *{message.reply_to_message.from_user.full_name}*-banned!\nBe vigilant.😈",
        parse_mode="Markdown"
    )
    await message.bot.delete_message(config.GROUP_ID, message.reply_to_message.message_id)
    await asyncio.sleep(3600)  # Message deletion timer == seconds
    await message_bot.delete()


# Bot command users i
@dp.message_handler(commands=["i"], commands_prefix="/", chat_id=config.GROUP_ID)
async def commands_info(message: types.Message):
    message_bot = await message.answer(
        f"*{message.from_user.full_name}*, Information!👇", reply_markup=urlkb,
        parse_mode="Markdown")
    await message.bot.delete_message(config.GROUP_ID, message.message_id)
    await asyncio.sleep(3600)  # Message deletion timer == seconds
    await message_bot.delete()


# bot command users help
@dp.message_handler(commands=["help"], commands_prefix="/", chat_id=config.GROUP_ID)
async def commands_help(message: types.Message):
    message_bot = await message.answer(
        f"*{message.from_user.full_name}*, if you need help, write to the chat administrator📲. *I'm on vacation*🏖.",
        parse_mode="Markdown")
    await message.bot.delete_message(config.GROUP_ID, message.message_id)
    await asyncio.sleep(3600)  # Message deletion timer == seconds
    await message_bot.delete()


# Simple profanity check words
@dp.message_handler(chat_id=config.GROUP_ID)
async def filter_messages(message: types.Message):
    if message.from_user.id == owner_id:
        return

    if {i.lower().translate(str.maketrans(' ', ' ', string.punctuation)) for i in message.text.split(' ')} \
            .intersection(
        set(json.load(open('cens.json')))) != set():  # List of obscene expressions in Russian and English
        message_bot = await message.reply(
            f"Forbidden Word❌!!!\nYou *{message.from_user.full_name}* - have the wrong chat room😡!",
            parse_mode="Markdown"
        )
        await message.bot.delete_message(config.GROUP_ID, message.message_id)
        await asyncio.sleep(3600)  # Message deletion timer == seconds
        await message_bot.delete()

    if "admin" in message.text:  # Forwarding a message with the text "admin", to the chat administrator.
        await bot.forward_message(chat_id=config.OWNER_ID, from_chat_id=config.GROUP_ID, message_id=message.message_id)


# Left chat member
@dp.message_handler(content_types=["left_chat_member"], chat_id=config.GROUP_ID)
async def left_member(message: types.Message):
    left_member = message.left_chat_member
    message_bot = await message.answer(f"*{left_member.mention}*, left the chat room 🚀.", parse_mode="Markdown")
    await message.bot.delete_message(config.GROUP_ID, message.message_id)
    await asyncio.sleep(10800)  # Message deletion timer == seconds
    await message_bot.delete()


# Bot command start error chat ID + echo bot
@dp.message_handler(commands=["start"])
async def commands_start(message: types.Message):
    if message.from_user.id == owner_id:
        await message.answer(f"*{message.from_user.full_name}*, I know you and you know me!\nHello 👻.",
                             parse_mode="Markdown")
        await message.delete()
        return

    await message.reply(
        f"❌*{message.from_user.full_name}*,the *WITH-AUTHORITY function is ACTIVATED*!!!",
        "\nYou're - *a stranger*.!\nYou have *1 minute* to delete the chat!!!🧨⏳",
        parse_mode="Markdown"
    )
    await asyncio.sleep(60)  # Message deletion timer == seconds
    await message.answer("The minute has passed, I warned You❗️")
    await message.delete()


# Mirror echo bot
@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text[::-1])


# Run long-polling
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
