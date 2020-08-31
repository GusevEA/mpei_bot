#   Description
#       Telegram Bot:
#       name: myMPEI_bot
#       photo: mpei.jpg
#       short_name: myMPEI
#       token: 1242069093:AAFZr78T1oihvVurSNdzX_4cCmA7qECqDw0
#       making requests: https://api.telegram.org/bot<token>/METHOD_NAME (/getMe)
#       deleteWebHook: https://api.telegram.org/bot1242069093:AAFZr78T1oihvVurSNdzX_4cCmA7qECqDw0/deleteWebhook
#       setWebHook: https://api.telegram.org/bot1242069093:AAFZr78T1oihvVurSNdzX_4cCmA7qECqDw0/setWebhook?url=
#                   https://telegg.ru/orig/bot1242069093:AAFZr78T1oihvVurSNdzX_4cCmA7qECqDw0/setWebhook?url=


from flask import Flask
from flask import request
from flask import jsonify
from flask_sslify import SSLify

import requests
import json
import pandas as pd
import schedule
import threading
import time
import bars
import messages
import mailmpei

app = Flask(__name__)
sslify = SSLify(app)

token = '1242069093:AAFZr78T1oihvVurSNdzX_4cCmA7qECqDw0'
# url = 'https://api.telegram.org/bot' + token
url = 'https://telegg.ru/orig/bot' + token
__connection = None


def write_json(data, filename='data.json'):
    with open(filename, 'w') as f:
        try:
            json.dump(data, f, indent=2, ensure_ascii=False)
        except:
            pass


def send_message(chat_id, text='Думаю...'):
    send = url + '/sendMessage'
    answer = {'chat_id': chat_id,
              'text': text}

    r = requests.post(send, json=answer)
    return r.json()


def df_from_excel(filename):
    xl = pd.ExcelFile(filename)
    df = xl.parse()

    return df


def get_data(chat_id, df):
    login = {'chat_id': chat_id}

    if len(df[df.chat_id == chat_id].values) == 0:
        df.loc[len(df), 'chat_id'] = chat_id
        df.loc[df[df.chat_id == chat_id].index, 'login'] = '-'
        df.loc[df[df.chat_id == chat_id].index, 'password'] = '-'
        send_message(chat_id, messages.hello())
        time.sleep(1)

    else:
        if df[df.chat_id == chat_id].password.values[0] != '-':
            login = {'chat_id': chat_id,
                     'login': df[df.chat_id == chat_id].login,
                     'password': df[df.chat_id == chat_id].password}

        elif df[df.chat_id == chat_id].login.values[0] != '-':
            login = {'chat_id': chat_id,
                     'login': df[df.chat_id == chat_id].login}

    return login


def write_data(df, filename):
    writer = pd.ExcelWriter(filename, engine='xlsxwriter')

    # Write your DataFrame to a file
    df.to_excel(writer, 'Sheet1', index=False)

    # Save the result
    writer.save()


def set_data(chat_id, df_bars, df_reg, message):
    if len(df_reg[df_reg.chat_id == chat_id]) >= 1:
        reg_stage = df_reg[df_reg.chat_id == chat_id].reg_stage.values

        if reg_stage == 1:
            df_bars.loc[df_bars[df_bars.chat_id == chat_id].index, 'login'] = message
        elif reg_stage == 2:
            df_bars.loc[df_bars[df_bars.chat_id == chat_id].index, 'password'] = message
            df_reg.loc[df_reg[df_bars.chat_id == chat_id].index, 'reg_stage'] = 3

    else:
        df_reg.loc[len(df_reg), 'chat_id'] = chat_id


def reg_message(stage, df_reg, chat_id):
    if stage == 1:
        send_message(chat_id, messages.login('process'))
        time.sleep(0.5)
        send_message(chat_id, messages.login('login'))
        if len(df_reg[df_reg.chat_id == chat_id]) == 1:
            df_reg.loc[df_reg[df_reg.chat_id == chat_id].index, 'reg_stage'] = 1

    elif stage == 2:
        send_message(chat_id, messages.login('password'))
        df_reg.loc[df_reg[df_reg.chat_id == chat_id].index, 'reg_stage'] = 2


def notification():
    df = df_from_excel('data_mail.xlsx')

    for ind in range(len(df)):
        login = df.loc[ind]['login']
        password = df.loc[ind]['password']
        html = mailmpei.auth(login, password)
        new_mail = mailmpei.is_new_mail(html)
        data = mailmpei.update_data(login, password, new_mail)

        if data is not False:

            chat_id = data[0]
            new_num = data[1]

            if int(new_num) == 1:
                message_data = mailmpei.mailfrom(html)[0]

            else:
                message_data = mailmpei.mailfrom(html)[:int(new_num)]
                message_data = '\n\n'.join(message_data)

            send_message(chat_id, messages.notification(message_data, new_mail) + messages.next())


schedule.every(3).seconds.do(notification)


def go():
    while 1:
        try:
            schedule.run_pending()
        except:
            print('NoneType')
        time.sleep(1)


t = threading.Thread(target=go, name="тест")
t.start()


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        r = request.get_json()
        write_json(r, 'post.json')
        chat_id = r['message']['chat']['id']
        try:
            message = r['message']['text']
        except:
            message = '/info'

        df_bars = df_from_excel('data_bars.xlsx')
        df_reg = df_from_excel('reg_logs.xlsx')

        set_data(chat_id, df_bars, df_reg, message)

        write_data(df_bars, 'data_bars.xlsx')
        df_bars = df_from_excel('data_bars.xlsx')

        login = get_data(chat_id, df_bars)

        stage = len(login)
        print(message)

        if stage == 3:
            html_bars = bars.auth(login['login'], login['password'])
            try:
                user = bars.get_name(html_bars)
                is_registr = 1
            except:
                is_registr = 0
                user = ' '  # для удобства

            if is_registr == 1:

                sem_data = bars.get_subjects(html_bars)
                subjects = bars.parse_subjects(sem_data)

                # Основные команды
                if message == '/mydata':
                    send_message(chat_id, messages.my_data(user) + messages.next())

                elif message == '/mysubjects':

                    send_message(chat_id, messages.mysubjects(subjects) + messages.next())

                elif message == '/logout':
                    df_bars.loc[df_bars[df_bars.chat_id == chat_id].index, 'login'] = '-'
                    df_bars.loc[df_bars[df_bars.chat_id == chat_id].index, 'password'] = '-'
                    df_reg.loc[df_reg[df_bars.chat_id == chat_id].index, 'reg_stage'] = '-'

                    df_mail = df_from_excel('data_mail.xlsx')

                    if len(df_mail[df_mail.chat_id == chat_id]) != 0:
                        df_mail.drop(df_mail[df_mail.chat_id == chat_id].index, inplace=True)
                        write_data(df_mail, 'data_mail.xlsx')


                    send_message(chat_id, messages.logout())
                    time.sleep(0.5)
                    send_message(chat_id, messages.login('relogin'))

                elif message == '/dashboard':
                    pass

                elif message == '/info':
                    send_message(chat_id, messages.info())

                elif message == '/stat':
                    for ind in range(len(subjects)):
                        sub_dict = bars.get_subjectdata(html_bars, ind)
                        send_message(chat_id, '/' + str(ind + 1) + '- ' + subjects[ind] +
                                     '\n\n' + '📈  Балл тек. контроля: '
                                     + sub_dict['point'])  # перевести в messages
                        time.sleep(0.15)

                    time.sleep(2)
                    send_message(chat_id, messages.next(in_mes=True))


                elif message == '/setnotification':
                    df_mail = df_from_excel('data_mail.xlsx')

                    if len(df_mail[df_mail.chat_id == chat_id]) == 0:
                        df_mail.loc[len(df_mail)] = {
                            'chat_id': chat_id,
                            'login': df_bars[df_bars.chat_id == chat_id]['login'].values[0],
                            'password': df_bars[df_bars.chat_id == chat_id]['password'].values[0],
                            'new_mail': '0'
                        }

                        write_data(df_mail, 'data_mail.xlsx')
                        send_message(chat_id, messages.setnotification() + messages.next())
                    else:
                        send_message(chat_id, messages.setnotification(repeat=True) + messages.next())

                elif message == '/resetnotification':

                    df_mail = df_from_excel('data_mail.xlsx')

                    if len(df_mail[df_mail.chat_id == chat_id]) != 0:
                        df_mail.drop(df_mail[df_mail.chat_id == chat_id].index, inplace=True)
                        write_data(df_mail, 'data_mail.xlsx')
                        send_message(chat_id, messages.resetnotification() + messages.next())
                    else:
                        send_message(chat_id, messages.resetnotification(repeat=True) + messages.next())

                elif message == '/mail':

                    html_mail = mailmpei.auth(login['login'], login['password'])

                    try:
                        num = mailmpei.is_new_mail(html_mail)
                        is_good = 1
                    except:
                        is_good = 0
                        num = ''

                    if is_good == 1:
                        message_data = mailmpei.mailfrom(html_mail)
                        send_message(chat_id, messages.new_mail(num, message_data) + messages.next())

                    else:
                        # Неверный логин или пароль
                        pass
                # Информация по предметам
                elif len(message) == 2 or len(message) == 3:

                    try:
                        if len(message) == 2:
                            n = int(message[1])
                        else:
                            n = int(message[1:])

                        if n < len(subjects) + 1 and n > 0:
                            is_command = 1
                        else:
                            is_command = 0
                    except:
                        n = 0  # чтобы не ругался
                        is_command = 0

                    if is_command == 1:
                        sub_dict = bars.get_subjectdata(html_bars, n - 1)
                        if len(sub_dict['name']) != 0:
                            send_message(chat_id, '***  ' + subjects[n - 1] + '  ***')
                            for i in range(len(sub_dict['name'])):
                                send_message(chat_id, messages.subjectdata(sub_dict, i))

                            send_message(chat_id, messages.point(sub_dict) + messages.back() +
                                         messages.next())

                        else:
                            send_message(chat_id, '***  ' + subjects[n - 1] + '  ***')
                            send_message(chat_id, messages.notfound())
                            time.sleep(1)
                            send_message(chat_id, messages.info())
                    else:
                        send_message(chat_id, messages.info())

                else:
                    send_message(chat_id, messages.info())

            else:
                send_message(chat_id, messages.error())
                df_bars.loc[df_bars[df_bars.chat_id == chat_id].index, 'login'] = '-'
                df_bars.loc[df_bars[df_bars.chat_id == chat_id].index, 'password'] = '-'
                df_reg.loc[df_reg[df_bars.chat_id == chat_id].index, 'reg_stage'] = '-'


        elif stage > 1 or message == '/login':
            reg_message(stage, df_reg, chat_id)

        else:
            send_message(chat_id, messages.login('relogin'))

        write_data(df_reg, 'reg_logs.xlsx')
        write_data(df_bars, 'data_bars.xlsx')

        return jsonify(r)
    return '<h1>Welcome</h1>'


if __name__ == '__main__':
    app.run()
