import requests
from bs4 import BeautifulSoup
import re
from lxml import html as hl


def auth(log, pas):
    url = 'https://bars.mpei.ru/bars_web/'

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
        'Password': pas,
        'Remember': False,
        'UserName': log
    })

    html_txt = post_request.text

    return html_txt


def is_registr(html):
    soup = BeautifulSoup(html, 'lxml')
    text = soup.find('div', class_='col-12 alert alert-danger text-center').text.strip()
    print(text)


def get_name(html):
    soup = BeautifulSoup(html, 'lxml')
    name = soup.find('span', class_='font-weight-bold').text.strip().split()
    course = soup.find('li', class_='list-inline-item').text.strip().split()
    user = {
        'second_name': name[0],
        'first_name': name[1],
        'group': name[6],
        'course': course[-1]
    }

    return user


def get_subjects(html):
    soup = BeautifulSoup(html, 'lxml')
    sem_data = soup.find('div', id='div-Student_SemesterSheet').text.strip()
    return sem_data


def parse_subjects(data):
    sub_re = re.compile(r'Дисциплина(.*)\(')
    subjects = sub_re.findall(data)

    for ind in range(len(subjects)):
        subjects[ind] = subjects[ind].strip()

    return subjects


def get_subjectdata(html, n):
    tree = hl.fromstring(html)
    # //*[@id="s_ss_' + str(n) + '"]/div/table/tbody/tr[2]/td[1]/text()

    # n = 2
    table_path = '//*[@id="s_ss_' + str(n) + '"]/div/table/tbody'

    # a = tree.xpath(table_path + '/tr[2]/td[1]/text()')[0].strip()
    # print(a)

    length_col = len(tree.xpath(table_path + '/tr')) - 5

    rating_dict = {
        'name': [],
        'volume': [],
        'week': [],
        'rate': [],
    }

    for col in range(2, length_col):
        for row in range(1, 5):
            try:
                data = tree.xpath(table_path + f'/tr[{col}]/td[{row}]/text()')[0].strip()
            except:
                data = '-----'
            rating_dict[list(rating_dict.keys())[row - 1]].append(data)

    try:
        data = tree.xpath(table_path + f'/tr[{length_col}]/td[2]/text()')[0].strip()
        rating_dict['point'] = data
    except:
        rating_dict['point'] = '-----'

    return rating_dict

def main():
    login = '---'
    password = '----'

    html = auth(login, password)
    # print(html)
    # data = get_name(html)
    # print(data)

    sem_data = get_subjects(html)

    sub = get_subjectdata(html, 0)

    print(sub)
    # subjects = parse_subjects(sem_data)
    # print(subjects)

    # print(subjects)


if __name__ == '__main__':
    main()
