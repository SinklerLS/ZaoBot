from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext

import tgbot.keyboards.reply as rkb
from tgbot.filters.user_type import UserTypeFilter
from .group_edit_form import send_group_edit_form
from tgbot.misc.states import GroupEditingStates


async def handle_student_list_interaction(callback_query: CallbackQuery, state: FSMContext):
    cq_data = callback_query.data
    # state_data = await state.get_data()
    # del_msgs = state_data["del_msgs"]

    # for msg in del_msgs:
        # await msg.delete()
    await state.update_data(del_msgs=[])

    if cq_data == 'back':
        await send_group_edit_form(callback_query.message, state)
    elif cq_data == 'cancel':
        await callback_query.message.answer("Меню менеджера", reply_markup=rkb.manager_keyboard)
        await state.finish()


def register_student_list_interaction(dp):
    dp.register_callback_query_handler(
        handle_student_list_interaction,
        UserTypeFilter("manager"),
        state=GroupEditingStates.student_list_interaction
        )