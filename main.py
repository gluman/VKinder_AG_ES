import datetime as d
import json
import time
from pprint import pprint as pp
import requests
from vk_api.longpoll import VkEventType

from vkbot_connect import longpoll
from vkbot_connect import write_msg


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


def input_value_for_search():   # Нужно переделать для телеграмм бота
    # age = int(input('Введите возраст: '))
    # sex = input('Введите пол(м/ж): ')
    # city = input('Введите город для поиска:')
    pass



def justwork():
    Run = True
    pp('Прежде чем начать изучи README.md')
    scenario = ''
    while Run:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:

                if event.to_me:
                    request = event.text
                    if request == "help" and scenario == '':
                        write_msg(event.user_id, f'help - вывод данной справки')
                        write_msg(event.user_id, f'find - ввод критериев и поиск')
                        write_msg(event.user_id, f'show - просмотр ранее полученных результатов')
                        write_msg(event.user_id, f'quit - выход из программы')

                    elif request == "find":
                        write_msg(event.user_id, f'Укажите возраст для поиска (от 18 до 99):')
                        scenario = 'get_age'
                    elif type(request) == int and 18 <= int(request) <= 99 and scenario == 'get_age':
                        age = int(request)
                        scenario = 'get_sex'

                    elif request in ['м', 'ж']:
                        sex = request
                        scenario = 'get_city'

                    elif len(request) >= 3:
                        city = request

                    elif request == "quit":
                        write_msg(event.user_id, "Спасибо за использование программы. До свидания!")
                        Run = False

                    elif request == 'clear':
                        scenario = ''

                    elif scenario != '':
                        write_msg(event.user_id, "Повторите ввод! Или начать всё сначала(clear)")

                    else:
                        write_msg(event.user_id, "Введенные данные не распознаны! Начать всё сначала: clear")







        # command = input('Введите команду(help - справка):')
        # if command == 'help':
        #     pp('help - вывод данной справки'
        #        'find - ввод критериев и поиск'
        #        'show - просмотр ранее полученных результатов'
        #        'quit - выход из программы')
        # elif command == 'find':
        #     input_value_for_search()
        # elif command == 'quit':
        #     pp('Спасибо за использование программы. До свидания!')
        #     Run = False
        # elif command == 'show':
        #     pass
        # else:
        #     pp('Команда не распознана! ')


if __name__ == '__main__':
    justwork()

