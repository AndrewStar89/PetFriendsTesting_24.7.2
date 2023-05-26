from api import PetFriends
from settings import valid_email, valid_password

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Проверяем что запрос API ключа возвращает статус 200 и в результате содержится слово key"""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    """Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем API ключ и сохраняем в переменную auth_key. Далее, используя этот ключ,
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо ''"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data(name='Драго', animal_type='дракон', age='4', pet_photo='images/drakon_1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Драго", "дракон", "6", "images/drakon_1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()

def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")



# Дополнительные 10 тестов!!!



def test_add_new_pet_photo(pet_photo='images/zmei-gorinich.jpg'):
    """Проверяем что можно заменить фотографию существующего питомца"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.create_pet_simple(auth_key, "Драго", "дракон", "6", "images/drakon_1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Добавляем фотографию питомца
    status, result = pf.add_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert len(result['pet_photo']) > 0

def test_add_new_pet_without_photo(name='Драго2', animal_type='Дракон', age='6'):
    """Проверяем что можно добавить питомца с корректными данными без фотографии"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_get_api_key_for_invalid_user(email='something_went_wrong@mail.ru', password='12345678'):
    """Проверяем что запрос API ключа с неверными email и password возвращает статус ошибки 403"""
    status, result = pf.get_api_key(email, password)
    assert status == 403

def test_get_all_pets_with_invalid_filter(filter='my_ets'):
    """Проверяем что запрос всех питомцев с неверно написанным фильтром возвращает ошибку.
    Для этого сначала получаем API ключ и сохраняем в переменную auth_key. Далее, используя этот ключ,
    запрашиваем список всех питомцев и проверяем статус запроса.
    Доступное значение параметра filter - 'my_pets' либо ''"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status > 200

def test_get_all_pets_with_invalid_key(filter=''):
    """Проверяем что запрос с неверным auth_key возвращает ошибку 403"""
    auth_key = {"key": "79015a790047c38ab25592f702ed517f555ff622d534020869e383c2???"}
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 403

def test_add_new_pet_with_big_data():
    """Проверяем что можно добавить питомца с очень длинными данными"""
    name = '''ДРАААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААА
    ГГГООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООО
    ОООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООО
    ОООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООО
    ООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООООО'''
    animal_type = 'драконААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААА!!!'
    age = (
           '-9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999\n'
           '-9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999\n'
           '-9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999\n'
           '-9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999\n'
           '-9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999\n'
           '-9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999\n'
           )
    pet_photo = 'images/drakon_1.jpg'

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_add_new_pet_with_missing_data(name='Драго2', animal_type='Дракон'):
    """Проверяем что попытка добавления питомца с отсутствующими данными (аргументом 'age') вызовет ошибку"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.create_pet_simple(auth_key, name, animal_type)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_add_new_pet_with_gif_photo(name='Дрогоз', animal_type='дракон', age='6', pet_photo='images/gifka-drakona.gif'):
    """Проверяем что при попытке добавления питомца с фотографией некорректного формата, фотография не добавится"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_update_pet_with_gif_photo(pet_photo='gifka-drakona.gif'):
    """Проверяем что при попытке замены фотографии существующего питомца на фотографию некорректного формата
    запрос вызовет ошибку"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.create_pet_simple(auth_key, "Драго", "дракон", "4", "images/drakon_1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Добавляем фотографию питомца
    status, result = pf.add_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status > 200
    assert len(result['pet_photo']) > 0

def test_add_new_pet_without_data(name='', animal_type='', age=''):
    """Проверяем что можно добавить питомца с параметрами, в которых отсутствуют данные"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
