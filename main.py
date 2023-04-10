import datetime as d
import json
import time
from pprint import pprint as pp
import requests

from Settings import VK_TOKEN as vk_token
from Settings import base_vk_link as vk_link

def connected_vk(): # Подключаемся к VK
    pass

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

