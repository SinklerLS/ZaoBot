from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

import tgbot.keyboards.inline as ikb
import tgbot.keyboards.reply as rkb
from tgbot.models.db import Database
from tgbot.misc.states import PersonalDataChangeStates
from tgbot.filters.user_type import UserTypeFilter
from tgbot.models.database_instance import db


async def send_login_command(message: Message, state: FSMContext):
    msgs_to_del = [await message.answer(text="<b>Пожалуйста введите новый логин</b>",
                                        reply_markup=rkb.login_input_cancel_keyboard)]
    await state.update_data(msgs_to_del=msgs_to_del)
    await PersonalDataChangeStates.get_new_login_state.set()


async def send_password_check_command(message: Message, state: FSMContext):
    msgs_to_del = [await message.answer(text="<b>Пожалуйста введите текущий пароль</b>",
                                        reply_markup=rkb.login_input_cancel_keyboard)]
    await state.update_data(chat_id=message.chat.id, msgs_to_del=msgs_to_del)
    await PersonalDataChangeStates.check_password_state.set()


async def get_new_login(message: Message, state: FSMContext):
    bot = message.bot
    chat_id = message.from_user.id
    new_login = message.text
    await clear_chat(message, state, 1)
    login_list = await db.get_user_logins()
    is_added = 0
    for login in login_list:
        if new_login == login[0]:
            msgs_to_del = [await bot.send_message(text=f"<b>Такой логин уже занят. Пожалуйста введите новый логин:</b>",
                                                  chat_id=chat_id)]
            await state.update_data(msgs_to_del=msgs_to_del)
            is_added = 1
            break
    if is_added:
        await PersonalDataChangeStates.get_new_login_state.set()
    else:
        await state.update_data(new_login=new_login)
        msgs_to_del = [
            await bot.send_message(text=f"<b>Вы уверены, что хотите сменить логин на:</b> {new_login}<b>?</b>",
                                   chat_id=chat_id, reply_markup=ikb.confirm_name_kb)]
        await state.update_data(msgs_to_del=msgs_to_del)
        await PersonalDataChangeStates.confirm_login_change_state.set()


async def confirm_login_change(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await clear_chat(callback_query.message, state, 0)
    role = await db.get_user_type(callback_query.from_user.id)
    if callback_query.data == "yes":
        data = await state.get_data()
        new_login = data.get("new_login")
        await db.change_login(callback_query.from_user.id, new_login)
        if role == "manager":
            await callback_query.message.answer(text="<b>Логин успешно изменен</b>\n\n<b>Меню менеджера</b>",
                                                reply_markup=rkb.manager_keyboard)
        elif role == "teacher":
            await callback_query.message.answer(text="<b>Логин успешно изменен</b>\n\n<b>Меню преподавателя</b>",
                                                reply_markup=rkb.teacher_keyboard)
        else:
            await callback_query.message.answer(text="<b>Логин успешно изменен</b>\n\n<b>Меню студента</b>",
                                                reply_markup=rkb.student_keyboard)
    else:
        if role == "manager":
            await callback_query.message.answer(text="<b>Отмена\n\nМеню менеджера</b>",
                                                reply_markup=rkb.manager_keyboard)
        elif role == "teacher":
            await callback_query.message.answer(text="<b>Отмена</b>\n\n<b>Меню преподавателя</b>",
                                                reply_markup=rkb.teacher_keyboard)
        else:
            await callback_query.message.answer(text="<b>Отмена</b>\n\n<b>Меню студента</b>",
                                                reply_markup=rkb.student_keyboard)
    await state.finish()


async def check_password(message: Message, state: FSMContext):
    bot = message.bot
    chat_id = message.from_user.id
    password = message.text
    await clear_chat(message, state, 1)
    real_password = await db.get_password(chat_id)
    if password == real_password:
        msgs_to_del = [await bot.send_message(text="<b>Пароль подтвержден. Введите новый пароль:</b>", chat_id=chat_id)]
        await state.update_data(msgs_to_del=msgs_to_del)
        await PersonalDataChangeStates.get_new_password_state.set()
    else:
        msgs_to_del = [await bot.send_message(text="<b>Пароль введен неверно. Пожалуйста введите текущий пароль:</b>",
                                              chat_id=chat_id)]
        await state.update_data(msgs_to_del=msgs_to_del)
        await PersonalDataChangeStates.check_password_state.set()


async def get_new_password(message: Message, state: FSMContext):
    bot = message.bot
    chat_id = message.from_user.id
    new_password = message.text
    await clear_chat(message, state, 1)
    await state.update_data(new_password=new_password)
    msgs_to_del = [await bot.send_message(
        text=f"<b>Вы уверены, что хотите сменить ваш пароль на:</b> {new_password}<b>?</b>",
        chat_id=chat_id, reply_markup=ikb.confirm_name_kb)]
    await state.update_data(msgs_to_del=msgs_to_del)
    await PersonalDataChangeStates.confirm_new_password_state.set()


async def confirm_new_password(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    data = await state.get_data()
    role = await db.get_user_type(callback_query.from_user.id)
    await clear_chat(callback_query.message, state, 0)
    if callback_query.data == "yes":
        new_password = data.get("new_password")
        await db.change_password(callback_query.from_user.id, new_password)
        if role == "manager":
            await callback_query.message.answer(text="<b>Пароль успешно изменен</b>\n\n<b>Меню менеджера.</b>",
                                                reply_markup=rkb.manager_keyboard)
        elif role == "teacher":
            await callback_query.message.answer(text="<b>Пароль успешно изменен</b>\n\n<b>Меню преподавателя.</b>",
                                                reply_markup=rkb.teacher_keyboard)
        else:
            await callback_query.message.answer(text="<b>Пароль успешно изменен</b>\n\n<b>Меню студента.</b>",
                                                reply_markup=rkb.student_keyboard)
    else:
        if role == "manager":
            await callback_query.message.answer(text="<b>Меню менеджера</b>",
                                                reply_markup=rkb.manager_keyboard)
        elif role == "teacher":
            await callback_query.message.answer(text="<b>Меню преподавателя</b>",
                                                reply_markup=rkb.teacher_keyboard)
        else:
            await callback_query.message.answer(text="<b>Меню студента</b>",
                                                reply_markup=rkb.student_keyboard)
    await state.finish()


async def clear_chat(message: Message, state: FSMContext, del_user_msg):
    data = await state.get_data()
    msgs_to_del = data.get("msgs_to_del")
    for msg in msgs_to_del:
        await msg.delete()
    if del_user_msg:
        await message.delete()


def register_personal_data_change(dp):
    dp.register_message_handler(send_login_command, ~UserTypeFilter(None), content_types=['text'],
                                text=['Сменить логин'])
    dp.register_message_handler(send_password_check_command, ~UserTypeFilter(None),
                                content_types=['text'], text=['Сменить пароль'])
    dp.register_message_handler(get_new_login, state=PersonalDataChangeStates.get_new_login_state)
    dp.register_callback_query_handler(confirm_login_change, state=PersonalDataChangeStates.confirm_login_change_state)
    dp.register_message_handler(check_password, state=PersonalDataChangeStates.check_password_state)
    dp.register_message_handler(get_new_password, state=PersonalDataChangeStates.get_new_password_state)
    dp.register_callback_query_handler(confirm_new_password, state=PersonalDataChangeStates.confirm_new_password_state)
