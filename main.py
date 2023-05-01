from vk_api.longpoll import VkEventType
from vkbot_connect import longpoll, VK_SEARCH, write_msg
from db_connect import save_person_to_db, save_value_for_search, save_result,save_result_photo,  update_result
from Settings import vk_user_token, count_filtred_search
import pprint


# Отбираем только три человека у которых профиль открыт.
def filter_partners(info, count):
    partners_items = info['response']['items']

    for item in partners_items:
        if item['is_closed'] == True:
            partners_items.remove(item)
            continue
    return partners_items[0:count]

# Отбираем только три лучше фотографии
def filter_free_best_photos(photos):
    free_bets_photos = []
    count_likes = 0
    for photo in photos:
        if photo['likes']['count'] > 0:
            count = photo['likes']['count']
            id_photo = photo['id']
            for size in photo['sizes']:
                if size['type'] == 'x':
                    url_photo = size['url']
            if url_photo == '':
                url_photo = photo['sizes'][-1]['url']


            free_bets_photos.append([count, id_photo, url_photo])

    free_bets_photos.sort().reverse()
    return free_bets_photos[0:3]



def get_and_save_photo(list_):
    for item in list_: # проходим по каждому из найденых людей.
        owner_id = item['partner_id']
        photos = item['partner_photos']['response']['items']
        free_best_photos = filter_free_best_photos(photos)




if __name__ == '__main__':
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
                        # Сохраняем id пользователя.
                        id_row_user_id = save_person_to_db(event.user_id)

                        # создаем экземпляр класса VK
                        vk_search = VK_SEARCH(vk_user_token, event.user_id)

                        # Делаем запрос в VK c передаваемыми параметрами, полученный результат
                        result_search_raw = vk_search.search_users(age, sex, city)

                        result_search_normal = filter_partners(result_search_raw, count_filtred_search)

                        # Сохраняем полученные результаты в БД
                        save_result(result_search_normal, event.user_id, sex, age, city)

                        # Запрашиваем фотографии по ранее найденным людям.
                        result_get_photos = vk_search.vk_get_partners_photos(result_search_normal)

                        # Сохраняем найденные фотографии в БД.
                        get_and_save_photo(result_get_photos)

                        update_result(result_get_photos)



                    elif request == "quit":
                        write_msg(event.user_id, "Спасибо за использование программы. До свидания!")
                        Run = False

                    elif request == 'clear':
                        scenario = ''

                    elif scenario != '':
                        write_msg(event.user_id, "Повторите ввод! Или начать всё сначала: clear")

                    else:
                        write_msg(event.user_id, "Введенные данные не распознаны! help - справка. clear - ч")




