def decorator(func):
    def wrapper():
        print('Пожалуйста, подождите. Идёт сбор данных...')
        func()
        print('Сбор данных окончен!')

    return wrapper
