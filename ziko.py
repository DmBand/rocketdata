import requests
import json
from bs4 import BeautifulSoup


def get_data(url_html, url_api):
    # Т.к. в api нет телефонных номеров, то их берём с HTML страницы
    response_html = requests.get(url=url_html)
    # Парсим HTML-страницу и забираем таблицу с контактами
    soup = BeautifulSoup(response_html.text, 'html.parser')
    contacts = soup.find_all('td', attrs={'class': 'mp-table-address'})
    # Т.к. на одном адресе может быть до 3-х компаний (Ziko Apteka, Ziko Optyk, Ziko Dermo),
    # то телефоны этих компаний будут разложены по разным спискам
    phones = {}
    for contact in contacts:
        all_contacts = str(contact).split('<br/>')
        # Ключом будет адрес, взятый с HTML-страницы
        key = f'{all_contacts[0][29:].strip()}'
        if key not in phones:
            phones[f'{key}'] = [all_contacts[-2].strip()[5:].split(';')]
        else:
            phones[key] += [all_contacts[-2].strip()[5:].split(';')]

    # Далее открываем на запись json-файл, формируем данные для записи и записываем их
    with open('ziko.json', 'w', encoding='utf8') as f:
        data = []
        # Обращемся уже к api и забираем данные в json-формате
        response_api = requests.get(url=url_api)
        pharmacies = response_api.json()
        # Пробегаем циклом по всем аптекам и для каждой формируем свой словарь с данными
        for p in pharmacies:
            pharmacy = {
                'address': pharmacies[p].get('address').strip(),
                'latlon': [pharmacies[p].get('lat'), pharmacies[p].get('lng')],
                'name': pharmacies[p].get('title'),
                'phones': phones.get(pharmacies[p].get('address').strip()),
                'working_hours': []
            }
            # Т.к. на одном адресе иожет быть несколько учреждений, то проверяем их наличие.
            # Если учреждение есть, то его график работы записываем в отдельный список
            apteka = pharmacies[p].get('mp_pharmacy_hours') if pharmacies[p].get('mp_pharmacy_enabled') == 'enabled' else None
            optyk = pharmacies[p].get('mp_optyk_hours') if pharmacies[p].get('mp_optyk_enabled') == 'enabled' else None
            dermo = pharmacies[p].get('mp_dermo_hours') if pharmacies[p].get('mp_dermo_enabled') == 'enabled' else None
            if apteka:
                pharmacy['working_hours'].append([apteka.replace('<br>', ', ').strip()])
            if optyk:
                pharmacy['working_hours'].append([optyk.replace('<br>', ', ').strip()])
            if dermo:
                pharmacy['working_hours'].append([dermo.replace('<br>', ', ').strip()])

            # Добавляем словарь с данными для одной аптеки в общий список,
            # а затем записываем этот список в финальный json-файл
            data.append(pharmacy)
        json.dump(obj=data, fp=f, ensure_ascii=False, indent=4)


def main():
    print('Пожалуйста, подождите. Идёт сбор данных...')
    url_html = 'https://www.ziko.pl/lokalizator/'
    url_api = 'https://www.ziko.pl/wp-admin/admin-ajax.php?action=get_pharmacies'
    get_data(url_html=url_html, url_api=url_api)
    print('Сбор данных окончен!')


if __name__ == '__main__':
    main()
