import requests
import pandas as pd
from bs4 import BeautifulSoup
import re


def auth(log, pas):
    url = 'https://mail.mpei.ru/CookieAuth.dll?Logon'

    user_agent_val = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
                     'AppleWebKit/537.36 (KHTML, like Gecko)' \
                     'Chrome/75.0.3770.142' \
                     'Safari/537.36'

    session = requests.Session()
    session.get(url, headers={
        'User-Agent': user_agent_val
    })

    session.headers.update({'Referer': url})
    session.headers.update({'User-Agent': user_agent_val})

    post_request = session.post(url, {
        'curl': 'Z2FowaZ2F',
        'flags': 0,
        'forcedownlevel': 0,
        'formdir': 2,
        'username': log,
        'password': pas,
        'isUtf8': 1,
        'trusted': 4

    })

    html_txt = post_request.text
    return html_txt


def is_new_mail(html):
    soup = BeautifulSoup(html, 'lxml')

    num = soup.find('span', class_='unrd')
    if num is not None:
        num = num.text.strip()
        sub_re = re.compile(r'\((.*)\)')
        num = sub_re.findall(num)[0]
    else:
        num = '0'
    return num


def mailfrom(html):
    soup = BeautifulSoup(html, 'lxml')

    message_data = []

    for data in soup.find_all('tr', style='font-weight:bold;'):
        data = data.text.strip().split('\xa0')
        del data[-1]
        data = f'От: {data[0]}\n' \
            f'Тема: {data[1]}\n' \
            f'Время: {data[2]} {data[3]}'

        message_data.append(data)

    return message_data


def get_df():
    xl = pd.ExcelFile('data_mail.xlsx')
    df = xl.parse()
    return df


def set_df(df):
    writer = pd.ExcelWriter('data_mail.xlsx', engine='xlsxwriter')
    df.to_excel(writer, 'Sheet1', index=False)
    writer.save()


def update_data(login, password, new_mail):
    df = get_df()
    if len(df[(df.login == login) & (df.password == password)].values) == 1:
        data_mails = df[(df.login == login) & (df.password == password)].new_mail.values[0]

        if int(new_mail) > int(data_mails):
            chat_id = str(df[(df.login == login) & (df.password == password)].chat_id.values[0])

            new_num = str(int(new_mail) - int(data_mails))

            df.loc[df[(df.login == login) & (df.password == password)].index, 'new_mail'] = str(
                int(data_mails) + int(new_num))

            set_df(df)

            data = [chat_id, new_num]

            if chat_id is not None and new_num is not None:
                return data
            else:
                return False
        else:
            df.loc[df[(df.login == login) & (df.password == password)].index, 'new_mail'] = int(new_mail)
            set_df(df)

            return False


def main():
    login = 'GusevYegA'
    password = 'huf283a'
    html = auth(login, password)
    new_mail = is_new_mail(html)
    # print(mailfrom(html))
    # print(new_mail)
    print(update_data(login, password, new_mail))


if __name__ == '__main__':
    main()
