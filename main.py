from vk_api.longpoll import VkEventType
from vkbot_connect import longpoll, VK_SEARCH, write_msg
from db_connect import save_person_to_db, save_value_for_search
from Settings import vk_user_token
import pprint

def justwork():
    Run = True

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
                        #     пишем данные персоны (пользователя, с которым взаимодействуем)
                        save_person_to_db(event.user_id)  # Сохраняем id пользователя.
                        save_value_for_search(event.user_id, age, sex, city)  # cохраняем пролученные значения параметров поиска в бд
                        vk_search = VK_SEARCH(vk_user_token, event.user_id) # создаем экземпляр класса VK
                        result = vk_search.search_users(age, sex, city)  # Делаем запрос в VK c передаваемыми параметрами, полученный результат
                        pprint(result)


                    elif request == "quit":
                        write_msg(event.user_id, "Спасибо за использование программы. До свидания!")
                        Run = False

                    elif request == 'clear':
                        scenario = ''

                    elif scenario != '':
                        write_msg(event.user_id, "Повторите ввод! Или начать всё сначала: clear")

                    else:
                        write_msg(event.user_id, "Введенные данные не распознаны! help - справка. clear - ч")


if __name__ == '__main__':
    justwork()
