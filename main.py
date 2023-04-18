import datetime as d
import json
import time
from pprint import pprint as pp
import requests


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
    age = int(input('Введите возраст: '))
    sex = input('Введите пол(м/ж): ')
    city = input('Введите город для поиска:')




def justwork():
    Run = True
    pp('Прежде чем начать изучи README.md')


    while Run:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:

                if event.to_me:
                    request = event.text

                    if request == "привет":
                        write_msg(event.user_id, f"Хай, {event.user_id}")
                    elif request == "пока":
                        write_msg(event.user_id, "Пока((")
                    else:
                        write_msg(event.user_id, "Не поняла вашего ответа...")






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

