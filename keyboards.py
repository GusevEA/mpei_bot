# Клавиатура для бота

from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup

from telegram import ReplyKeyboardMarkup

TITLES = {
    'MY_DATA': '🔒  Мои данные',
    'MY_SUBJECTS': '🎓  Мои дисциплины',
    'STAT': '📈  Текущий контроль',
    'MAIL': '📮  Почта',
    'HELP': '✈  Помощь',
    'LOGOUT': 'Выйти',
}

CALL_BACK_BUTTON_MYDATA = 'call_back_button_mydata'
CALL_BACK_BUTTON_MYSUBJECTS = 'call_back_button_mysubjects'
CALL_BACK_BUTTON_STAT = 'call_back_button_stat'
CALL_BACK_BUTTON_HELP = 'call_back_button_help'
CALL_BACK_BUTTON_MAIL = 'call_back_button_mail'
CALL_BACK_BUTTON_LOGOUT = 'call_back_button_logout'

CALL_BACK_BUTTON_MENU = 'call_back_button_mune'


def get_keyboard():
    keyboard = [[InlineKeyboardButton(TITLES['MY_DATA'], callback_data=CALL_BACK_BUTTON_MYDATA)],
                [InlineKeyboardButton(TITLES['MY_SUBJECTS'], callback_data=CALL_BACK_BUTTON_MYSUBJECTS)],
                [InlineKeyboardButton(TITLES['STAT'], callback_data=CALL_BACK_BUTTON_STAT)],
                [InlineKeyboardButton(TITLES['MAIL'], callback_data=CALL_BACK_BUTTON_MAIL)],
                [InlineKeyboardButton(TITLES['HELP'], callback_data=CALL_BACK_BUTTON_HELP)],
                [InlineKeyboardButton(TITLES['LOGOUT'], callback_data=CALL_BACK_BUTTON_LOGOUT)]
                ]

    return ReplyKeyboardMarkup(keyboard)

