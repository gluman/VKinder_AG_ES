import json
import shutil

from vk_api.longpoll import VkEventType
from vkbot_connect import longpoll, VK, write_msg, write_attach, upload
from db_connect import \
    db_save_person_to_db, \
    db_save_result, \
    db_save_photo_to_db,  \
    db_get_partners, \
    db_get_current_partner, \
    db_attach_current_partner_photo, \
    db_change_favorites
from Settings import vk_user_token, count_filtred_search
import os
from time import sleep
import requests
import pprint


# Отбираем только три человека у которых профиль открыт.
def main_filter_partners(info, count):
    partners_items = info['response']['items']
    filtred_partners = []
    for item in partners_items:
        if item['is_closed'] == True:
            continue
        else:
            filtred_partners.append(item)


    return filtred_partners[0:count]

# Отбираем только три лучше фотографии
def main_filter_free_best_photos(photos):
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

def main_tempory_save_photos(owner_id, photos, _source):  # Сохраняем верменно локально фотографии по одному найденному человеку.
    if not os.path.exists('Tempary_saved_photos'):
        os.mkdir('Tempary_saved_photos')
    photo_folder = os.path.join(f'Tempary_saved_photos', f'{owner_id}')
    if not os.path.exists(photo_folder):
        os.mkdir(photo_folder)
    for photo in photos: # сохраняем локально каждое фото в папку с id человека
        if _source == 'vk':
            r = requests.get(photo['url_photo'])
            with open(os.path.join(photo_folder, '%s.jpg' % photo['id_photo']), 'wb') as f:
                for buf in r.iter_content(1024):
                    if buf:
                        f.write(buf)
        elif _source == 'folder':
            with open(os.path.join(photo_folder, '%s.jpg' % photo[2]), 'wb') as f:
                f.write(photo[3])

        sleep(1)
    return True


def main_get_and_save_photo(list_):
    for item in list_: # проходим по каждому из найденых людей.
        owner_id = item['partner_id']
        photos = item['partner_photos']['response']['items']
        free_best_photos = main_filter_free_best_photos(photos)
        if main_tempory_save_photos(owner_id, free_best_photos, 'vk'):
            db_save_photo_to_db(owner_id, free_best_photos)

def main_get_partners(criteria, owner_id):
    partners = db_get_partners(criteria, owner_id)
    return partners

def main_current_partner(id):
    current_partner = db_get_current_partner(id)
    return current_partner

def main_attach_current_partner_photo(id):
    photos = db_attach_current_partner_photo(id)
    if main_tempory_save_photos(id, photos, 'folder'):
        return True




# def get_profile_link(partners):
#     for partner in partners:
#         profile_link = vk_search.get_users_info(partner['id'])
#         _link = profile_link[0]
#         db_update_profile_link(partner['id'], _link)
#     return True






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
                        write_msg(event.user_id, f'show - > next - показать следующего человека')
                        write_msg(event.user_id, f'show - > add - добавить в избранные')
                        write_msg(event.user_id, f'show - > rem - удалить из избранных')
                        write_msg(event.user_id, f'show - > del - удалить из БД>')
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
                        id_row_user_id = db_save_person_to_db(event.user_id)

                        # создаем экземпляр класса VK
                        vk_search = VK(vk_user_token, event.user_id)

                        # Делаем запрос в VK c передаваемыми параметрами, полученный результат
                        result_search_raw = vk_search.search_users(age, sex, city)
                        result_search_normal = main_filter_partners(result_search_raw, count_filtred_search)
                        if len(result_search_normal) >=1:

                        # Сохраняем полученные результаты в БД
                            db_save_result(result_search_normal, event.user_id, sex, age, city)

                            # Запрашиваем фотографии по ранее найденным людям.
                            result_get_photos = vk_search.vk_get_partners_photos(result_search_normal)

                            # Сохраняем найденные фотографии в БД.
                            main_get_and_save_photo(result_get_photos)
                            write_msg(event.user_id, f"Отобрано {len(result_search_normal)} человек(-а).")
                            # write_msg(event.user_id, f"Показать резултаты? (yes - да, no - нет")
                            # scenario = 'get_after_find'


                        else:
                            write_msg(event.user_id, "Никого не найдено, задайте другие критерии поиска")
                            scenario = ''
                            request = "find"

                    # elif request == 'yes' and scenario == 'get_after_find':
                    #     req




                    elif request == 'show':
                        write_msg(event.user_id, "Показать только избранных(top)? или всех(all)?")
                        scenario = 'show'

                    elif (request == 'top' or
                          request == 'all' or
                          request == 'next' or
                          request == 'rem' or
                          request == 'add' or
                          request == 'del'):

                        if request == 'top' or request == 'all':
                            db_partners = main_get_partners(request, event.user_id)
                            if len(db_partners) > 0:
                                index = 0
                                partner = db_partners[index]
                                write_msg(event.user_id, f'Имя и фамилия: {partner[3]} {partner[4]}')
                                write_msg(event.user_id, f'Ссылка на профиль: {partner[6]}')
                                attach = main_attach_current_partner_photo(partner[0])
                                temp_folder = os.path.join('Tempary_saved_photos', str(partner[0]))
                                files = os.listdir(path=temp_folder)

                                for file in files:
                                    write_attach(event.user_id, 'Фото:', os.path.join(temp_folder, file))
                                shutil.rmtree(temp_folder)
                                write_msg(event.user_id, f'next: следующий/ add_favorite: в избранное/ delete: удалить/ clear: вначало')
                                scenario = 'show'
                            else:
                                write_msg(event.user_id,
                                          f'Ничего нет в БД')


                        elif len(db_partners) > 0 and request == 'next' and scenario =='show':
                            if index >= len(db_partners)-1:
                                write_msg(event.user_id, "Готово!")
                                request = 'clear'
                            elif len(db_partners) == 0:
                                write_msg(event.user_id,
                                          f'Ничего нет в БД')
                                request = 'clear'
                            else:
                                index += 1
                                partner = db_partners[index]
                                write_msg(event.user_id, f'Имя и фамилия: {partner[3]} {partner[4]}')
                                write_msg(event.user_id, f'Ссылка на профиль: {partner[6]}')
                                attach = main_attach_current_partner_photo(partner[0])
                                temp_folder = os.path.join('Tempary_saved_photos', str(partner[0]))
                                files = os.listdir(path=temp_folder)

                                for file in files:
                                    write_attach(event.user_id, 'Фото:', os.path.join(temp_folder, file))
                                shutil.rmtree(temp_folder)
                                write_msg(event.user_id,
                                          f'next: следующий/ add_favorite:в избранное/ delete: удалить/ clear: вначало')

                        elif (request == 'add' or request == 'rem') and scenario == 'show':
                            id_partner = partner[0]
                            if db_change_favorites(id_partner, request):
                                write_msg(event.user_id, 'Добавлено в избранные')


                        elif request == 'del' and scenario == 'show':
                            pass



                    elif request == "quit":
                        write_msg(event.user_id, "Спасибо за использование программы. До свидания!")
                        Run = False

                    elif request == 'clear':
                        scenario = 'help'


                    else:
                        write_msg(event.user_id, "Введенные данные не распознаны!")
                        write_msg(event.user_id, f"Текущий контекст: {scenario}")
                        write_msg(event.user_id, f'help - для спарвки')





