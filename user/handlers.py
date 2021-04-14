import os
from time import strftime

from aiogram import types


async def log_file(message: types.Message):
    os.makedirs("./logs/", exist_ok=True)

    with open(f"./logs/{message.chat.id}.csv", "a+", encoding="utf-8") as f:
        data = [
            strftime("%Y-%m-%d %H:%M:%S"),
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
            message.from_user.id,
            message.text,
            message.contact
        ]
        f.write(f"{';'.join(map(str, data))}\n")