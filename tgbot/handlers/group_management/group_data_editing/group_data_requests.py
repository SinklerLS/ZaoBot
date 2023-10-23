from aiogram.types import Message
from aiogram.dispatcher import FSMContext

import tgbot.keyboards.reply as rkb
from tgbot.misc.states import GroupNameChangeStates, GroupURLChangeStates


async def request_new_group_name(message: Message, state: FSMContext):
    await message.answer(text="Введите новое название группы:",
                         reply_markup=rkb.url_change_cancel_keyboard)
    await GroupNameChangeStates.getting_new_group_name.set()


async def request_new_performance_list_url(message: Message, state: FSMContext):
    await message.answer(text="Введите новую ссылку на таблицу успеваемости:",
                         reply_markup=rkb.url_change_cancel_keyboard)
    await GroupURLChangeStates.getting_new_performance_list_url.set()