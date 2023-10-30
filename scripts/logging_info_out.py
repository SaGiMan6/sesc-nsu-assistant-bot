from aiogram.types import Message


def logging_output(message: Message):
    print(f"Chat id: {message.chat.id}, " +
          f"User id: {message.from_user.id}, " +
          f"Username: {message.from_user.id}")
    print(f"First name: {message.from_user.first_name}, " +
          f"Last name: {message.from_user.last_name}")
