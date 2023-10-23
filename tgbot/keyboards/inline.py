from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.models.db import Database
import datetime
from tgbot.models.database_instance import db

confirmation_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Да', callback_data='yes'),
            InlineKeyboardButton(text='Нет', callback_data='no')
        ]
    ]
)


user_type_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Менеджер', callback_data='manager'),
            InlineKeyboardButton(text='Преподаватель', callback_data='teacher')
        ]
    ]
)

confirm_name_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Да', callback_data='yes'),
        ],
        [
            InlineKeyboardButton(text='Нет', callback_data='no')
        ]
    ]
)


teacher_mailing_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Ввести сообщение', callback_data='mailing_text_input'),
            InlineKeyboardButton(text='Выбрать группы', callback_data='groups_selection'),
        ],
        [
            InlineKeyboardButton(text='Ввести дату', callback_data='date_input'),
            InlineKeyboardButton(text='Ввести время', callback_data='time_input')
        ],
        [
            InlineKeyboardButton(text='Подтвердить и отправить', callback_data='confirmation_of_mailing'),
            InlineKeyboardButton(text='Отмена', callback_data='cancellation_of_mailing_form')
        ]
    ]
)

manager_mailing_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Ввести сообщение', callback_data='mailing_text_input'),
            InlineKeyboardButton(text='Выбрать группы', callback_data='groups_selection'),
        ],
        [
            InlineKeyboardButton(text='Ввести дату', callback_data='date_input'),
            InlineKeyboardButton(text='Выбрать менеджеров', callback_data='managers_selection'),
        ],
        [
            InlineKeyboardButton(text='Ввести время', callback_data='time_input'),
            InlineKeyboardButton(text='Выбрать преподавателей', callback_data='teachers_selection'),
        ],
        [
            InlineKeyboardButton(text='Подтвердить и отправить', callback_data='confirmation_of_mailing'),
            InlineKeyboardButton(text='Отмена', callback_data='cancellation_of_mailing_form')
        ]
    ]
)


async def courses_kb_generator():
    groups = await db.get_group_names()
    courses_buttons_list = []
    courses_list = []
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month
    for gr in groups:
        if gr[0].isdigit():
            year_of_admission = str(current_year // 100) + gr[0][:2]
        else:
            year_of_admission = str(current_year // 100) + gr[0][-2:]
        if current_month < 9:
            course = current_year - int(year_of_admission)
        else:
            course = current_year - int(year_of_admission) + 1
        if course not in courses_list:
            courses_list.append(course)
    courses_list.sort()
    for course in courses_list:
        courses_buttons_list += [InlineKeyboardButton(text="Курс " + str(course),
                                                      callback_data="course_" + str(course))]

    course_selection_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            courses_buttons_list,
            [
                InlineKeyboardButton(text='Подтвердить', callback_data='course_select_confirm')
            ]
        ]
    )
    return course_selection_keyboard


group_edit_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Сменить название группы", callback_data='change_group_name'),
            InlineKeyboardButton(text="Сменить таблицу успеваемости", callback_data='change_performance_list')
        ],
        [
            InlineKeyboardButton(text="Список студентов", callback_data='display_student_list'),
            InlineKeyboardButton(text="Обновить студентов", callback_data='update_student_list')
        ],
        [
            InlineKeyboardButton(text="Отмена", callback_data='cancel_group_editing')
        ]
    ]
)

student_list_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Назад", callback_data='back'),
            InlineKeyboardButton(text="Отмена", callback_data='cancel'),
        ]
    ]
)