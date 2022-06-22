import requests
import json
import decorator


def get_data(url):
    # Все нужные данные хранятся в api, поэтому будем работать с ним
    response = requests.get(url=url)
    # Открываем на запись новый json-файл, формируем данные для записи и записываем их
    with open('kfc.json', 'w', encoding='utf8') as f:
        data = []
        restaurants = response.json().get('searchResults')
        # Проходим циклом по всем ресторанам
        for r in restaurants:
            # Т.к. в api есть пустые словари (видимо, тестовые данные какие-то),
            # то их в финальный файл записывать не будем.
            # Т.е., если адреса у заведения нет, то его пропускаем
            address = r.get('storePublic').get('contacts').get('streetAddress').get('ru')
            if address is not None:
                restaurant = {
                    'address': address,
                    'latlon': r.get('storePublic').get('contacts').get('coordinates').get('geometry').get('coordinates'),
                    'name': r.get('storePublic').get('title').get('ru'),
                    'phones': r.get('storePublic').get('contacts').get('phoneNumber')
                }
                # Если ресторан временно закрыт, то записываем "closed"
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

                # Добавляем словарь с данными для одного ресторана в общий список,
                # а затем записываем этот список в финальный json-файл
                data.append(restaurant)
        json.dump(obj=data, fp=f, ensure_ascii=False, indent=4)


@decorator.decorator
def main():
    url = 'https://api.kfc.com/api/store/v2/store.get_restaurants?showClosed=true'
    get_data(url=url)


if __name__ == '__main__':
    main()
