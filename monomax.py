import requests
import json
import re
from bs4 import BeautifulSoup


def get_data(url):
    # Т.к. сайт не отдаёт никаких полезных json-файлов,
    # то всю информацию будем брать c html-страницы
    response = requests.get(url=url)
    soup = BeautifulSoup(response.text, 'lxml')
    # Получаем список адресов, телефонов и очищаем его от ненужных данных
    addresses = soup.find_all('p', attrs={'class': 'name'})
    phones = soup.find_all('p', attrs={'class': 'phone'})
    addresses_text = [a.text for a in addresses]
    phones_text = [p.text for p in phones if p.text]
    # Т.к. координаты магазина находятся в теге <script> и таких тегов на странице несколько,
    # то находим их все и берём самый последний
    script = soup.find_all('script', attrs={'type': 'text/javascript'})[-1].text
    # По регулярному выражению находим все списки, в которых вначале обязательно идут 2 цифры
    pattern = r'\[\d{2}.*\]'
    coordinates = re.findall(pattern, script)[1:]

    # Далее открываем на запись json-файл, формируем данные для записи и записываем их
    with open('monomax.json', 'w', encoding='utf8') as f:
        data = []
        # Из собранных данных формируем словарь для каждого отдельного магазина
        for i in range(0, len(addresses_text)):
            store = {
                'address': addresses_text[i],
                'latlon': coordinates[i],
                'name': 'Мономах',
                'phones': phones_text[i]
            }

            # Добавляем словарь с данными для одного магазина в общий список,
            # а затем записываем этот список в финальный json-файл
            data.append(store)
        json.dump(obj=data, fp=f, ensure_ascii=False, indent=4)


def main():
    print('Пожалуйста, подождите. Идёт сбор данных...')
    url = 'https://monomax.by/map'
    get_data(url=url)
    print('Сбор данных окончен!')


if __name__ == '__main__':
    main()
