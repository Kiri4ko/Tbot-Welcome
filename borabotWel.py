#Bot for chat's Welcome V1 
import config
import logging
import filters 
import asyncio

from aiogram import Bot, Dispatcher, executor, types

from filters import IsAdminFilter

from aiogram.types import ContentType, Message

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.dispatcher import filters

from aiogram.dispatcher.filters import CommandStart


#log level
logging.basicConfig (level = logging.INFO)  

#bot init
bot = Bot (token = config.TOKEN)
dp = Dispatcher (bot)
chat_id=config.GROUP_ID
owner_id=config.OWNER_ID

#button url
urlkb = InlineKeyboardMarkup (row_width=1)
urlButton = InlineKeyboardButton (text = 'ФОРМА 📬', url = 'https://')
urlButton2 = InlineKeyboardButton (text = 'Ссылки дома 📲', url = 'https://')
urlButton3 = InlineKeyboardButton (text = 'Правила чата ⚡️', url = 'https://')
urlkb.add (urlButton, urlButton2, urlButton3)

#welcome new users
@dp.message_handler (content_types=["new_chat_members"], chat_id=config.GROUP_ID)
async def on_users_joined (message: types.Message) :
    new_member = message.new_chat_members[0]
    message_bot=await message.answer (f"Добро пожаловать, *{new_member.mention}*✌️!\nЭто чат дома *Бора-Бора*🏝. Обязательно заполните *ФОРМУ*📬 (если Вы этого не сделали) нового участника чата.\nПросмотрите все полезные *cсылки* дома📲.", reply_markup = urlkb, parse_mode="Markdown")
    await message.bot.delete_message (config.GROUP_ID,message.message_id)
    await asyncio.sleep (82800)
    await message_bot.delete ()



#command start bot 
@dp.message_handler(filters.CommandStart(),chat_id=config.GROUP_ID)
async def command_start_handler(message: types.Message):
    message_bot=await message.answer (f'*Здравствуйтe {message.from_user.full_name}*🙂!\nЭто всё  - я ограничен строками кода 👨‍💻!\nИспользуйте команды: /i, /help.', parse_mode="Markdown")
    await message.bot.delete_message (config.GROUP_ID,message.message_id)
    await asyncio.sleep (3600)
    await message_bot.delete ()


# activate filters
dp.filters_factory.bind (IsAdminFilter) 

#ban command (admins only!)
@dp.message_handler (is_admin = True, commands = ["ban"], commands_prefix="!/", chat_id=config.GROUP_ID)
async def cmd_ban (message: types.Message) :
	if not message.reply_to_message:
		message_bot=await message.reply ("Функция Бан - активна.\nЕщё немного и правосудие восторжествует!⚖️")
		await asyncio.sleep (3600)
		await message.bot.delete_message (config.GROUP_ID,message.message_id)
		await message_bot.delete ()
		return

	await message.bot.delete_message (config.GROUP_ID, message.message_id)
	await message.bot.kick_chat_member (chat_id=config.GROUP_ID, user_id=message.reply_to_message.from_user.id)
	message_bot=await message.reply_to_message.reply (f"Участник чата *{message.reply_to_message.from_user.full_name}*-забенен(а)!\nБудьте бдительны.😈", parse_mode="Markdown")
	await message.bot.delete_message (config.GROUP_ID, message.reply_to_message.message_id)
	await asyncio.sleep (3600)
	await message_bot.delete ()


#bot command users i
@dp.message_handler (commands = ["i"], commands_prefix="/", chat_id=config.GROUP_ID)
async def commands_info (message: types.Message):
	message_bot=await message.answer (f"*{message.from_user.full_name}*, все самые информативные ссылки нашего дома!👇", reply_markup = urlkb, parse_mode="Markdown")
	await message.bot.delete_message (config.GROUP_ID,message.message_id)
	await asyncio.sleep (3600)
	await message_bot.delete ()



#bot command users help
@dp.message_handler (commands = ["help"], commands_prefix="/", chat_id=config.GROUP_ID)
async def commands_help (message: types.Message):
	message_bot=await message.answer (f"*{message.from_user.full_name}*, eсли Вам требуется помощь, напишите администратору чата📲@skybro. *Я в отпуске* 🏖.", parse_mode="Markdown")
	await message.bot.delete_message (config.GROUP_ID,message.message_id)
	await asyncio.sleep (3600)
	await message_bot.delete ()


#simple profanity check words 
@dp.message_handler(chat_id=config.GROUP_ID)
async def filter_messages (message: types.Message) :
	if message.from_user.id == owner_id :
		return

	if "хуй" in message.text: 
		message_bot=await message.reply (f"Запрещенное слово❌!!!\nВы *{message.from_user.full_name}*-ошиблись чатом😡!", parse_mode="Markdown")
		await message.bot.delete_message (config.GROUP_ID,message.message_id)
		await asyncio.sleep (7200)
		await message_bot.delete ()

	
	if "сука" in message.text:
		message_bot=await message.reply (f"Запрещенное слово❌!!!\nВы *{message.from_user.full_name}*-ошиблись чатом😡!", parse_mode="Markdown")
		await message.bot.delete_message (config.GROUP_ID,message.message_id)
		await asyncio.sleep (7200)
		await message_bot.delete ()


#left chat member
@dp.message_handler (content_types=["left_chat_member"],chat_id=config.GROUP_ID)
async def left_member (message: types.Message) :
	left_member=message.left_chat_member
	message_bot=await message.answer (f"*{left_member.mention}*, покинул(а) чат 🚀.", parse_mode="Markdown")
	await message.bot.delete_message (config.GROUP_ID,message.message_id)
	await asyncio.sleep (82800)
	await message_bot.delete ()


#bot command start error chat ID
@dp.message_handler (commands = ["start"])
async def commands_start (message: types.Message):
	if message.from_user.id == owner_id :
		await message.answer (f"*{message.from_user.full_name}*, я же Вас знаю, а Вы меня!\nПривет 👻.", parse_mode="Markdown")
		await message.delete ()
		return

	await message.reply (f"❌*{message.from_user.full_name}*,функция *СВОЙ-ЧУЖОЙ - АКТИВИРОВАНА*!!!\nВы - *ЧУЖОЙ*!\nУ Вас *1 минута* для удаления чата!!!🧨⏳", parse_mode="Markdown")
	await asyncio.sleep (60)
	await message.answer ("Минута прошла, я Вас предупреждал❗️")
	await message.delete ()


#forward message 
#@dp.message_handler ()
#async def commands_start (message: types.Message):
	#await bot.forward_message (chat_id=config.OWNER_ID, from_chat_id=config.GROUP_ID, message_id=message.message_id)

	
#run long-polling
if __name__ == "__main__" :
	
	executor.start_polling (dp, skip_updates=True)
