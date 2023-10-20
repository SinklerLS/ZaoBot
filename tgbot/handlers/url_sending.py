from aiogram import types
from tgbot.filters.user_type import UserTypeFilter
from tgbot.models.database_instance import db


async def send_schedule(message: types.Message):
    schedule_url = await db.get_schedule_url()
    if not schedule_url:
        await message.answer(text="<b>Ссылка на расписание еще не загружена менеджером!</b>")
    else:
        await message.answer(text=schedule_url)


async def send_work_schedule(message: types.Message):
    work_schedule_url = await db.get_work_schedule_url()
    if not work_schedule_url:
        await message.answer(text="<b>Ссылка на график работы еще не загружена менеджером!</b>")
    else:
        await message.answer(text=work_schedule_url)


async def send_learning_schedule(message: types.Message):
    learning_schedule_url = await db.get_learning_schedule_url()
    if not learning_schedule_url:
        await message.answer(text="<b>Ссылка на график учебы еще не загружена менеджером!</b>")
    else:
        await message.answer(text=learning_schedule_url)


async def send_mailings_table(message: types.Message):
    mailings_table_url = await db.get_mailings_url()
    if not mailings_table_url:
        await message.answer(text="<b>Ссылка на таблицу рассылок еще не загружена менеджером!</b>")
    else:
        await message.answer(text=mailings_table_url)


async def send_reports(message: types.Message):
    reports_url = await db.get_report_cards_url()
    if not reports_url:
        await message.answer(text="<b>Ссылка на ведомости еще не загружена менеджером!</b>")
    else:
        await message.answer(text=reports_url[0])


async def send_retakes(message: types.Message):
    retakes_url = await db.get_retake_cards_url()
    if not retakes_url:
        await message.answer(text="<b>Ссылка на ведомости пересдач еще не загружена менеджером!</b>")
    else:
        await message.answer(text=retakes_url[0])


def register_url_sending(dp):
    dp.register_message_handler(send_schedule, ~UserTypeFilter(None), content_types=['text'], text='Расписание')
    dp.register_message_handler(send_work_schedule, UserTypeFilter("teacher"), content_types=['text'],
                                text='График работы')
    dp.register_message_handler(send_work_schedule, UserTypeFilter("manager"), content_types=['text'],
                                text='График работы')
    dp.register_message_handler(send_learning_schedule, UserTypeFilter("student"), content_types=['text'],
                                text='График учебы')
    dp.register_message_handler(send_learning_schedule, UserTypeFilter("manager"), content_types=['text'],
                                text='График учебы')
    dp.register_message_handler(send_mailings_table, UserTypeFilter("manager"), content_types=['text'],
                                text=['Таблица рассылок'])
    dp.register_message_handler(send_mailings_table, UserTypeFilter("teacher"), content_types=['text'],
                                text=['Таблица рассылок'])
    dp.register_message_handler(send_reports, UserTypeFilter("manager"), content_types=['text'],
                                text=['Получить ведомости'])
    dp.register_message_handler(send_reports, UserTypeFilter("teacher"), content_types=['text'],
                                text=['Получить ведомости'])
    dp.register_message_handler(send_retakes, UserTypeFilter("manager"), content_types=['text'],
                                text='Получить пересдачи')
    dp.register_message_handler(send_retakes, UserTypeFilter("teacher"), content_types=['text'],
                                text='Получить пересдачи')
