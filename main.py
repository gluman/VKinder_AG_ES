from vk_api.longpoll import VkEventType
from vkbot_connect import longpoll, VK_SEARCH, write_msg
from db_connect import save_person_to_db, save_value_for_search, save_result,save_result_photo,  update_result
from Settings import vk_user_token, count_filtred_search
import pprint


def filter_partners(info, count):
    partners_items = info['response']['items']

    for item in partners_items:
        if item['is_closed'] == True:
            partners_items.remove(item)
            continue
    return partners_items[0:count]




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
                        id_row_user_id = save_person_to_db(event.user_id)  # Сохраняем id пользователя.
                        vk_search = VK_SEARCH(vk_user_token, event.user_id) # создаем экземпляр класса VK
                        result_search_raw = vk_search.search_users(age, sex, city)  # Делаем запрос в VK c передаваемыми параметрами, полученный результат
                        result_search_normal = filter_partners(result_search_raw, count_filtred_search)
                        save_result(result_search_normal, event.user_id, sex, age, city) # Сохраняем полученные результаты в БД
                        result_get_photos = vk_search.vk_get_partners_photos(result_search_normal) # Запрашиваем фотографии по ранее найденным людям.
                        save_result_photo(result_get_photo) # Сохраняем найденные фотографии в БД.
                        update_result(result_get_photos)
                        # pprint(result)


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
