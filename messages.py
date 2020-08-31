# Data messages
import time


def hello():
    message = 'Привет👋🏻\n\nУ меня много полезных функций, но для начала ты должен войти в БАРС'

    return message


def login(string):
    message = ''

    if string == 'process':
        message = 'Вход в систему БАРС'
    elif string == 'login':
        message = 'Введите логин:'
    elif string == 'password':
        message = 'Введите пароль:'
    elif string == 'relogin':
        message = 'Для входа в БАРС напишите /login'

    return message


def logout():
    message = 'Вы вышли из системы😔\nДо скорой встречи!'

    return message


def help():
    message = '✈  Используйте кнопки встроенной клавиатуры или выберете команду из списка:\n\n' \
              '/mydata - покажет выши данные\n' \
              '/mysubjects - покажет выши дисциплины\n' \
              '/stat- покажет балл тек. контроля по дисциплинам\n' \
              '/n - информация о дисциплине\n\t\t\t\t\t\t (Например: /1)\n' \
              '/mail - проверка почты\n' \
              '/logout - выйти из системы\n\n' \
              '👉🏻  Номера дисциплин можно посмотреть в /mysubjects или\n /stat\n\n' \
              '👉🏻  Чтобы получать уведомления о новых сообщениях перейдите в \n/mail'

    return message


def error():
    messages = 'Oops... 🙄\nОшибка в логине или пароле, войдите заново /login'

    return messages


def my_data(user):
    message = f'Студент: {user["second_name"]} {user["first_name"]}\n' \
        f'Группа: {user["group"]}\n' \
        f'Курс: {user["course"]}'

    return message


def mysubjects(mysub):
    i = 0
    for ind in range(len(mysub)):
        i += 1
        mysub[ind] = '/' + str(i) + '- ' + mysub[ind]

    mysub = '\n'.join(mysub)

    message = '''🎓  Ваши дисциплины:\n\n''' + mysub

    return message


def subjectdata(sub_dict, n):
    message = ''

    for key in sub_dict.keys():
        if key == 'name':
            message += sub_dict[key][n] + '\n\n'
        elif key == 'volume':
            message += '⚖  Вес: ' + sub_dict[key][n] + '\n\n'
        elif key == 'week':
            message += '📆  Неделя: ' + sub_dict[key][n] + '\n\n'
        elif key == 'rate':
            message += '✅  Оценка: ' + sub_dict[key][n]
        time.sleep(0.05)
    return message


def point(sub_dict):
    message = '📈  Балл текущего контроля: ' + sub_dict['point']
    return message


def new_mail(n, data):
    message = '📮  Непрочитанных писем: ' + str(n) + '\n\n'

    for ind in range(len(data)):
        message += '📩' + '\n' + data[ind] + '\n\n'

    message += 'Перейти в почту: https://mail.mpei.ru/CookieAuth.dll?GetLogon?curl=Z2FowaZ2FZ3FaeZ3DFolderZ26tZ' \
               '3DIPF.NoteZ26idZ3DLgAAAADx6NTVQidtTKoEWFyohO7QAQColniQu8cUQ5HizZ5ARyz6OAADrfZ2' \
               '52fRZ252fiAAABZ26slUsngZ3D0&reason=0&formdir=2\n\n' \
               '👉🏻  Хочу получать уведомления о новых сообщениях:\n\t\t\t/setnotification\n' \
               '👉🏻  Не хочу получать уведомления о новых сообщениях:\n\t\t\t/resetnotification'

    return message


def notification(message, num):
    message = 'Новое сообщение!\t📩\n\n' + message + \
              '\n\n📮Непрочитанных писем: ' + num + '\n\n' \
                                                  'Для перехода в почту: /mail'

    return message


def setnotification(repeat=None):
    if repeat == True:
        message = 'Уведомления уже подключены😌'
    else:
        message = 'Уведомления подключены😌'

    return message


def resetnotification(repeat=None):
    if repeat == True:
        message = 'Уведомления уже отключены😕'
    else:
        message = 'Уведомления отключены😕'

    return message


def notfound_mail():

    message = 'К сожалению, данная функция пока доступна только для тех, у кого ' \
              'логин и пароль почты совпадает с БАРСом😔'

    return message

def notfound():
    message = 'Данных нет'

    return message

