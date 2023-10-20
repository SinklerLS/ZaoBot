from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
import tgbot.keyboards.reply as rkb
from aiogram.types import Message
from tgbot.misc.decorators.log_decorator import log_function_call
from aiogram.dispatcher.filters import Text
from tgbot.models.database_instance import db


#  Оптимизировать конец функции
@log_function_call
async def cancel_all(message: Message, state: FSMContext):
    user_type = await db.get_user_type(message.from_user.id)
    if user_type == "student":
        await message.answer("Меню студента", reply_markup=rkb.student_keyboard)
    elif user_type == "teacher":
        await message.answer("Меню преподавателя", reply_markup=rkb.teacher_keyboard)
    elif user_type == "manager":
        await message.answer("Меню менеджера", reply_markup=rkb.manager_keyboard)
    else:
        await message.answer("Пожалуйста авторизируйтесь\n"
                             "Для этого воспользуйтесь командой /start", reply_markup=rkb.empty_keyboard)
    await state.finish()


def register_cancel(dp: Dispatcher):
    dp.register_message_handler(cancel_all, Text(equals="Отмена"), state="*")
    dp.register_message_handler(cancel_all, commands=['cancel'], state="*")
