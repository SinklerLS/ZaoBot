from aiogram.dispatcher.filters.state import StatesGroup, State


class AuthorizationStates(StatesGroup):
    login_waiting_state = State()
    password_waiting_state = State()
    data_check_state = State()


class FirstManagerAuthorizationStates(StatesGroup):
    name_waiting_state = State()
    authorization_state = State()


class ScheduleURLChangeStates(StatesGroup):
    change_schedule_url_state = State()


class WorkScheduleURLChangeStates(StatesGroup):
    change_work_schedule_url_state = State()

class LearningScheduleURLChangeStates(StatesGroup):
    change_learning_schedule_url_state = State()


class ReportsURLChangeStates(StatesGroup):
    change_reports_url_state = State()


class RetakesURLChangeStates(StatesGroup):
    change_retakes_url_state = State()


class MailingsURLChangeStates(StatesGroup):
    change_mailings_url_state = State()


class GroupAddStates(StatesGroup):
    get_group_name_state = State()
    get_group_address_state = State()


class GroupRefreshStates(StatesGroup):
    get_group_name_state = State()
    refresh_group_state = State()


class EmployeeAddStates(StatesGroup):
    name_waiting_state = State()
    user_type_selection_state = State()
    new_user_confirmation_state = State()


class ChangeUserPasswordStates(StatesGroup):
    select_user_to_change_password_state = State()
    select_group_to_change_password_state = State()
    get_new_user_password_state = State()


class PersonalDataChangeStates(StatesGroup):
    get_new_login_state = State()
    check_password_state = State()
    confirm_login_change_state = State()
    get_new_password_state = State()
    confirm_new_password_state = State()


class GroupsDelStates(StatesGroup):
    confirm_groups_deleting_state = State()
    deleting_groups_state = State()


class EmployeesDelStates(StatesGroup):
    confirm_deleting_state = State()
    deleting_employees_state = State()


# Перенастроить это
class MailingsStates(StatesGroup):
    mailing_form_interaction_state = State()
    mailing_text_input_state = State()
    course_selection_state = State()
    group_selection_state = State()
    teacher_selection_state = State()
    manager_selection_state = State()
    date_input_state = State()
    time_input_state = State()
