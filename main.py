import datetime as d
import json
import time
from pprint import pprint as pp
import requests
from vk_api.longpoll import VkEventType
import numbers
from vkbot_connect import longpoll
from vkbot_connect import write_msg
from vkbot_connect import VK_SEARCH, token
from db_connect import save_person_to_db





def save_person_information(user_id):
    vk_search = VK_SEARCH(token, user_id)
    person_data = vk_search.get_user_vkinfo(user_id)
    save_person_to_db()




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

                    elif request.isdigit() and scenario == 'get_age':
                        if 17 < int(request) and int(request) < 100:
                            age = int(request)
                            scenario = 'get_sex'
                            write_msg(event.user_id, f'Укажите пол для поиска (м или ж):')
                        else:
                            write_msg(event.user_id, f'Неверно задано значение, повторите ввод')

                    elif request in ['м', 'ж'] and scenario == 'get_sex':
                        sex = request
                        scenario = 'get_city'
                        write_msg(event.user_id, f'Укажите город для поиска (минимум 3 символа):')

                    elif len(request) >= 3 and scenario == 'get_city':
                        city = request
                        scenario = 'find_it'

                        save_person_information(event.user_id)

                        input_value_for_search(age, sex, city)


                    #     пишем данные персоны (пользователя, с которым взаимодействуем)

                    #   записываем в БД данные персоны и данные поиска.
                    #   формируем поисковые запросы через api vk
                    #   сохраняем полученные запросы в json
                    #   записываем полученные запросы в БД



                    elif request == "quit":
                        write_msg(event.user_id, "Спасибо за использование программы. До свидания!")
                        Run = False

                    elif request == 'clear':
                        scenario = ''

                    elif scenario != '':
                        write_msg(event.user_id, "Повторите ввод! Или начать всё сначала: clear")

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

