from vk_api.longpoll import VkEventType
from vkbot_connect import longpoll, VK_SEARCH, write_msg
from db_connect import save_person_to_db, save_result, save_photo_to_db,  update_result
from Settings import vk_user_token, count_filtred_search
import os
from time import sleep
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
    _photos = []
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


            _photos.append([count, id_photo, url_photo])

    _photos.sort()
    _photos.reverse()
    tempary_list_photos = _photos[0:3]
    free_bets_photos = []
    for i in tempary_list_photos:
        free_bets_photos.append({'likes': i[0], 'id_photo': i[1], 'url_photo': i[2]})

    return free_bets_photos

def tempory_save_photos(owner_id, photos):  # Сохраняем верменно локально фотографии по одному найденному человеку.
    if not os.path.exists('Tempary_saved_photos'):
        os.mkdir('Tempary_saved_photos')
    photo_folder = 'Tempary_saved_photos/'.format(owner_id)
    if not os.path.exists(photo_folder):
        os.mkdir(photo_folder)
    try:
        for photo in photos:
            r = request.get(photo['url_photo'], stream=True)
            with open(os.path.join(photo_folder, '%s.jpg' % photo['id_photo']), 'wb') as f:
                for buf in r.iter_content(1024):
                    if buf:
                        f.write(buf)
                        sleep(2)
        return 1
    except:
        return 0




def get_and_save_photo(list_):
    for item in list_: # проходим по каждому из найденых людей.
        owner_id = item['partner_id']
        photos = item['partner_photos']['response']['items']
        free_best_photos = filter_free_best_photos(photos)
        if tempory_save_photos(owner_id, free_best_photos):
            save_result_photo(owner_id, free_best_photos)



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
                        write_msg(event.user_id, "Введенные данные не распознаны!")
                        write_msg(event.user_id, f'help - вывод данной справки')
                        write_msg(event.user_id, f'find - ввод критериев и поиск')
                        write_msg(event.user_id, f'show - просмотр ранее полученных результатов')
                        write_msg(event.user_id, f'quit - выход из программы')




