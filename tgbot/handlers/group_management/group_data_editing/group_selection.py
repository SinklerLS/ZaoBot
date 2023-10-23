from aiogram.types import Message
from aiogram.dispatcher import FSMContext

import tgbot.keyboards.reply as rkb
from tgbot.filters.user_type import UserTypeFilter
from tgbot.misc.states import GroupEditingStates
from .group_edit_form import send_group_edit_form
from tgbot.models.database_instance import db


async def get_group_name(message: Message, state: FSMContext):
    groups = await db.get_group_names()
    if len(groups) == 0:
        await message.answer(text="Группы еще не добавлены", reply_markup=rkb.manager_keyboard)
    else:
        group_msg = ""
        for group in groups:
            group_msg += f"◦ `{group[0]}`;\n"

        del_msgs = [await message.answer(f"*Доступные группы:*\n{group_msg}\n"
                                         f"*Введите название группы, которую хотите выбрать*",
                                         reply_markup=rkb.group_name_cancel_keyboard, 
                                         parse_mode="MARKDOWN")]
        await state.update_data(del_msgs=del_msgs)
        await GroupEditingStates.getting_group_name.set()


async def check_group_name(message: Message, state: FSMContext):
    group_name = message.text
    group_name_list = await db.get_group_names()
    group_exist = False
    state_data = await state.get_data()
    del_msgs = state_data["del_msgs"]
    await del_msgs[0].delete()
    for group in group_name_list:
        if group[0] == group_name:
            group_exist = True
            await state.update_data(group_name=group_name)
            await send_group_edit_form(message, state)
    if not group_exist:
        await message.answer(text="<b>Такой группы не существует</b>")
    

def register_group_selection(dp):
    dp.register_message_handler(
        get_group_name, 
        UserTypeFilter("manager"), 
        content_types=['text'],
        text='Редактировать группу'
        ) 
    
    dp.register_message_handler(
        check_group_name, 
        state=GroupEditingStates.getting_group_name)