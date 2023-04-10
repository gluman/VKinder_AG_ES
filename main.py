import datetime as d
import json
import time
from pprint import pprint as pp
import requests

from Settings import VK_TOKEN as vk_token
from Settings import base_vk_link as vk_link

def connected_vk():
    pass


class VK:  # Подключаемся к VK
    def __init__(self, access_token, user_id, version='5.131'):
        self.token = access_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def users_info(self):
        url = vk_link + 'users.get'
        params = {'user_ids': self.id}
        response = requests.get(url, params={**self.params, **params})
        return response.json()

    def fotos_get(self, f_count, user_id, album='profile'):
        url = vk_link + 'photos.get'
        params = {'owner_id': user_id,
                  'album_id': album,
                  'extended': '1',
                  'photo_sizes': '1',
                  'count': f_count
                  }
        response = requests.get(url, params={**self.params, **params})
        return response.json()




def telegram_bot(): # Подключаемся к Telegram
    pass
def input_value_for_search():   # Нужно переделать для телеграмм бота
    age = int(input('Введите возраст: '))
    sex = input('Введите пол(м/ж): ')
    city = input('Введите город для поиска:')

def justwork():
    Run = True
    pp('Прежде чем начать изучи README.md')
    while Run:
        command = input('Введите команду(help - справка):')
        if command == 'help':
            pp('help - вывод данной справки'
               'find - ввод критериев и поиск'
               'show - просмотр ранее полученных результатов'
               'quit - выход из программы')
        elif command == 'find':
            input_value_for_search()
        elif command == 'quit':
            pp('Спасибо за использование программы. До свидания!')
            Run = False
        elif command == 'show':
            pass
        else:
            pp('Команда не распознана! ')


if __name__ == '__main__':
    justwork()

