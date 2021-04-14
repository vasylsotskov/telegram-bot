from datetime import date
from aiogram import Bot, Dispatcher, executor, types
from user import handlers

import config

# initialize bot
bot = Bot(token=config.TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

print("bot was started")

knownUsers = []


@dp.message_handler(commands='start')
async def start_command_handler(message: types.Message):
    cid = message.chat.id
    await handlers.log_file(message)

    if cid not in knownUsers:  # user has not send "/start" or bot was restarted :
        knownUsers.append(cid)
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        button_phone = types.KeyboardButton(text=" ☎ Send your phone number", request_contact=True)
        keyboard.add(button_phone)
        await bot.send_message(message.chat.id, text="send your number, there should be a ☎ button at the bottom",
                               reply_markup=keyboard)
    else:
        await bot.send_message(cid,
                               "Hello " + str(message.chat.first_name),
                               reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(content_types=['contact'])
async def contact(message):
    if message.contact.user_id != message.chat.id:  # if user id and number phone id is not equal
        # await log_file(message)
        await handlers.log_file(message)
        await bot.send_message(message.chat.id, "Sorry, could you send YOUR number, "
                                                "It`s easy just tap button under this message ☎ ")

    if message.contact.user_id == message.chat.id:  # if the user id matches the id of the phone number

        phone_number = message.contact.phone_number
        phone_7_digit = phone_number[-9::]

        # if we need check number frome txt file
        with open('staff-phone-numbers.txt', encoding='utf-8') as f:

            if phone_7_digit in f.read():
                await handlers.log_file(message)
                await bot.send_message(message.chat.id, text="👋🏻 ",
                                       reply_markup=types.ReplyKeyboardRemove())

            else:
                await bot.send_message(message.chat.id, text="Sorry but you are not yet our client 🤷‍♂️",
                                       reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(commands=['date'])
async def send_to_user_date(message):
    today = date.today()
    await handlers.log_file(message)
    await bot.send_message(message.chat.id, text=today)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
