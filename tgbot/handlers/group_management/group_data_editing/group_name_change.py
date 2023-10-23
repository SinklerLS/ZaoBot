from aiogram.types import Message
from aiogram.dispatcher import FSMContext

import tgbot.keyboards.reply as rkb
from tgbot.misc.states import GroupNameChangeStates
from tgbot.models.database_instance import db


async def check_new_group_name(message: Message, state: FSMContext):
    new_group_name = message.text
    group_name_list = await db.get_group_names()
    is_duplicate = 0
    for group_name in group_name_list:
        if group_name[0] == new_group_name:
            await message.answer("*Группа с таким названием уже существует!*\n\n"
                                 "*Введите другое название группы*",
                                 parse_mode="MARKDOWN")
            is_duplicate = 1
            break
    if not is_duplicate:
        await change_group_name(message, new_group_name, state)

        
async def change_group_name(message: Message, new_group_name, state = FSMContext):
    state_data = await state.get_data()
    group_name = state_data["group_name"]
    await db.change_group_name(group_name, new_group_name)
    await change_group_name_for_students(message, group_name, new_group_name, state)

# Менять название для всех студентов группы

async def change_group_name_for_students(message: Message, group_name, new_group_name, state = FSMContext):
    await db.change_group_name_for_students(group_name, new_group_name)
    await message.answer("*Название группы успешно изменено*",
                         parse_mode="MARKDOWN",
                         reply_markup=rkb.manager_keyboard)
    await state.finish()

def register_group_name_change(dp):
    dp.register_message_handler(
        check_new_group_name,
        content_types=['text'],
        state=GroupNameChangeStates.getting_new_group_name
        )