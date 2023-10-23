from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext

import tgbot.keyboards.reply as rkb
from tgbot.filters.user_type import UserTypeFilter
from .group_data_requests import request_new_group_name, request_new_performance_list_url
from .student_list_update import open_performance_list
from .student_list_display import send_student_list
from .group_edit_form import send_group_edit_form
from tgbot.misc.states import GroupEditingStates


async def handle_group_form_interaction(callback_query: CallbackQuery, state: FSMContext):
    cq_data = callback_query.data
    # state_data = await state.get_data()
    # del_msgs = state_data["del_msgs"]

    # for msg in del_msgs:
        # await msg.delete()
    # await state.update_data(del_msgs=[])

    if cq_data == 'change_group_name':
        await request_new_group_name(callback_query.message, state)
    elif cq_data == 'change_performance_list':
        await request_new_performance_list_url(callback_query.message, state)
    elif cq_data == 'update_student_list':
        # await open_performance_list(callback_query.message, state)
        await callback_query.answer("Эта функция пока не реализована")
        await send_group_edit_form(callback_query.message, state)    
    elif cq_data == 'display_student_list':
        await send_student_list(callback_query.message, state)
    elif cq_data == 'cancel_group_editing':
        await callback_query.message.answer("Меню менеджера", reply_markup=rkb.manager_keyboard)
        await state.finish()


def register_group_form_interaction(dp):
    dp.register_callback_query_handler(
        handle_group_form_interaction,
        UserTypeFilter("manager"),
        state=GroupEditingStates.group_form_interaction
        )