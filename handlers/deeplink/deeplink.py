from aiogram.dispatcher.filters import CommandStart
from aiogram import types, Dispatcher
from aiogram.utils.deep_linking import get_start_link


async def start_with_deep(message: types.Message):
    deep_link = await get_start_link(payload=str(message.from_user.id))
    await message.answer("deep_link 123 сработал!\n"
                         f"Ваша ссылка {deep_link}")


async def start_without_deep(message: types.Message):
    args = message.get_args()
    await message.answer(f"{args}")


def register_deeplink(dp: Dispatcher):
    dp.register_message_handler(start_with_deep, CommandStart(deep_link='123'))  #deep_link=re.compile(r"...") регулярное выражение
    dp.register_message_handler(start_without_deep, CommandStart())