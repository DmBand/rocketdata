import requests
import json


def get_data(url):
    response = requests.get(url=url)
    with open('ziko.json', 'w', encoding='utf8') as f:
        data = []
        pharmacies = response.json()
        for p in pharmacies:
            pharmacy = {
                'address': pharmacies[p].get('address'),
                'latlon': [pharmacies[p].get('lat'), pharmacies[p].get('lng')],
                'name': pharmacies[p].get('title'),
                'phones': pharmacies[p].get('tel'),
                'working_hours': pharmacies[p].get('mp_pharmacy_hours')
            }

            data.append(pharmacy)
        json.dump(obj=data, fp=f, ensure_ascii=False, indent=4)


def main():
    url = 'https://www.ziko.pl/wp-admin/admin-ajax.php?action=get_pharmacies'
    get_data(url=url)


if __name__ == '__main__':
    main()
