import requests
import json


def get_data(url):
    response = requests.get(url=url)
    with open('kfc.json', 'w', encoding='utf8') as f:
        data = []
        restaurants = response.json().get('searchResults')

        for r in restaurants:
            restaurant = {
                'address': r.get('storePublic').get('contacts').get('streetAddress').get('ru'),
                'latlon': r.get('storePublic').get('contacts').get('coordinates').get('geometry').get('coordinates'),
                'name': r.get('storePublic').get('title').get('ru'),
                'phones': r.get('storePublic').get('contacts').get('phoneNumber')
            }
            # Если ресторан временно закрыт, то записываем соответсвующие данные
            status = r.get('storePublic').get('status')
            if status.lower() != 'open':
                restaurant['working_hours'] = ['closed']
            else:
                start_time = r.get('storePublic').get('openingHours').get('regular').get('startTimeLocal')
                end_time = r.get('storePublic').get('openingHours').get('regular').get('endTimeLocal')
                # Если не указано время работы ресторана, то записываем, что данных нет
                if start_time is None and end_time is None:
                    restaurant['working_hours'] = ['Нет данных']
                else:
                    restaurant['working_hours'] = [
                        f'пн-пт {start_time} до {end_time}',
                        f'сб-вс {start_time} до {end_time}'
                    ]

            data.append(restaurant)
        json.dump(obj=data, fp=f, ensure_ascii=False, indent=4)


def main():
    url = 'https://api.kfc.com/api/store/v2/store.get_restaurants?showClosed=true'
    get_data(url=url)


if __name__ == '__main__':
    main()
