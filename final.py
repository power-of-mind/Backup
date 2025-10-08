
import requests
import sys
import time
from tqdm import tqdm

breed = input('Введите название породы: ').strip().lower()
token = input('Введите токен: ')
headers = {'Authorization': f'OAuth {token}'}

def get_breed():
    """Получение ссылки на изображение основной породы"""
    url_breed = f'https://dog.ceo/api/breed/{breed}/images/random'
    response = requests.get(url_breed)
    if response.status_code != 200 and response.json()['status'] == 'error':
        print('Такая порода не найдена')
        sys.exit(1)

    image_url = response.json()['message']
    file_name = breed + ' ' + image_url.split('/')[-1]
    return image_url, file_name

def get_sub_breeds():
    """Получение ссылок на изображения подпород"""
    url_sub_breeds = f'https://dog.ceo/api/breed/{breed}/list'
    response = requests.get(url_sub_breeds)
    list_all_sub_breeds = response.json()['message']

    image_url_sub_breeds_list = []

    if len(list_all_sub_breeds) > 0:
        for sub_breeds in list_all_sub_breeds:
            url_sub_breeds = f'https://dog.ceo/api/breed/{breed}/{sub_breeds}/images/random'
            response = requests.get(url_sub_breeds)
            image_url_sub_breeds = response.json()['message']
            image_url_sub_breeds_list.append(image_url_sub_breeds)
    return image_url_sub_breeds_list

def make_holder():
    """Создание папки на Яндекс Диске"""
    url_yandex_disk = 'https://cloud-api.yandex.net/v1/disk/resources'
    params = {
        "path": breed
    }
    requests.put(url_yandex_disk, headers=headers, params=params)

def upload_breed(image_url, file_name):
    """Загрузка изображения основной породы на диск"""
    upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
    params_1 = {
        'path': f'{breed}/{file_name}',
        'url': image_url
    }

    requests.post(upload_url, headers=headers, params=params_1)

def upload_sub_breeds(image_url_sub_breeds):
    """Загрузка изображений с подпородами на диск"""
    upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
    file_name_sub_breeds = breed + ' ' + image_url_sub_breeds.split('/')[-1]
    params_2 = {
        'path': f'{breed}/{file_name_sub_breeds}',
        'url': image_url_sub_breeds
    }

    requests.post(upload_url, headers=headers, params=params_2)

def download_files():
    """Главная функция, в которой вызываются вспомогательные функции"""
    make_holder()
    image_url, file_name = get_breed()
    upload_breed(image_url, file_name)
    image_url_sub_breeds_list = get_sub_breeds()

    for image_url_sub_breeds in image_url_sub_breeds_list:
        upload_sub_breeds(image_url_sub_breeds)

    mylist = [1, 2, 3, 4, 5, 6, 7, 8]
    for i in tqdm(mylist):
        time.sleep(1)

download_files()