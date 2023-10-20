import asyncio
import logging
from datetime import datetime
import pytz


from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from tgbot.filters.user_type import UserTypeFilter
from tgbot.middlewares.skip_handlers import SkipHandlerMiddleware
from tgbot.config import load_config
from tgbot.handlers.mailing.delayed_mailing_send import check_msgs_list
from tgbot.misc.commands import set_commands

from tgbot.handlers.cancel import register_cancel
from tgbot.handlers.menu import register_menu
from tgbot.handlers.authorization import register_authorization
from tgbot.handlers.logout import register_logout
from tgbot.handlers.URL_change.schedule_url import register_schedule_change
from tgbot.handlers.URL_change.work_schedule_url import register_work_schedule_change
from tgbot.handlers.URL_change.learning_schedule_url import register_learning_schedule_change
from tgbot.handlers.URL_change.mailings_url import register_mailings_link_change
from tgbot.handlers.URL_change.reports_url import register_reports_change
from tgbot.handlers.URL_change.retakes_url import register_retakes_change
from tgbot.handlers.performance_debts import register_performance_debts_check
from tgbot.handlers.users_editing.group_add import register_group_add
from tgbot.handlers.users_editing.employee_add import register_employee_add
from tgbot.handlers.users_editing.change_user_password import register_change_user_password
from tgbot.handlers.users_editing.groups_del import register_groups_del
from tgbot.handlers.users_editing.employees_del import register_employees_del
from tgbot.handlers.personal_data_change import register_pd_change
from tgbot.handlers.mailing.mailing_data_processing import register_mailing_data_processing
from tgbot.handlers.mailing.mailing_form_interaction import register_mailing_form_interaction
from tgbot.handlers.mailing.manager_mailing_form import register_manager_mailing_form
from tgbot.handlers.mailing.teacher_mailing_form import register_teacher_mailing_form
from tgbot.handlers.url_sending import register_url_sending
from tgbot.handlers.secret_commands import register_secret_command
from tgbot.handlers.users_editing.group_refresh import register_group_refresh

from tgbot.models.database_instance import db

logger = logging.getLogger(__name__)
timezone = pytz.timezone('Europe/Moscow')

def register_all_middlewares(dp, bot_start_time):
    dp.setup_middleware(SkipHandlerMiddleware(bot_start_time))


def register_all_filters(dp):
    dp.filters_factory.bind(UserTypeFilter)


def register_all_handlers(dp):
    register_cancel(dp)
    register_authorization(dp)
    register_logout(dp)
    register_menu(dp)
    register_schedule_change(dp)
    register_work_schedule_change(dp)
    register_learning_schedule_change(dp)
    register_mailings_link_change(dp)
    register_reports_change(dp)
    register_retakes_change(dp)
    register_performance_debts_check(dp)
    register_group_add(dp)
    register_employee_add(dp)
    register_change_user_password(dp)
    register_groups_del(dp)
    register_employees_del(dp)
    register_pd_change(dp)
    register_mailing_data_processing(dp)
    register_mailing_form_interaction(dp)
    register_manager_mailing_form(dp)
    register_teacher_mailing_form(dp)
    register_url_sending(dp)
    register_secret_command(dp)
    register_group_refresh(dp)


def set_scheduled_jobs(scheduler, bot):
    scheduler.add_job(check_msgs_list, "interval", seconds=60, args=(bot,))


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )

    bot_start_time = datetime.now(timezone).strftime('%Y-%m-%d %H:%M:%S')
    logger.info("Starting bot")
    config = load_config(".env")
    storage = MemoryStorage()

    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)
    bot['config'] = config
    scheduler = AsyncIOScheduler()

    set_scheduled_jobs(scheduler, bot)
    register_all_middlewares(dp, bot_start_time)
    register_all_filters(dp)
    register_all_handlers(dp)

    await db.create_tables()
    await set_commands(bot)

    try:
        scheduler.start()
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except(KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
