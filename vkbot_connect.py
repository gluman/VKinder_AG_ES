from random import randrange
import requests
import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from Settings import vk_group_token, vk_base_link as vk_link, count_raw_search, vk_group_id
from time import sleep
# token = input('Token: ')
gruop_token = vk_group_token

vk = vk_api.VkApi(token=gruop_token)
api = vk.get_api()

longpoll = VkLongPoll(vk)
upload = VkUpload(vk)
upload_url = api.photos.getMessagesUploadServer(group_id=vk_group_id, v='5.131')['upload_url']

def write_attach(id, message, file):
    upload_url = api.photos.getMessagesUploadServer(group_id=vk_group_id, v='5.131')['upload_url']
    request = requests.post(upload_url, files={'photo': open(file, "rb")})
    params = {
        'server': request.json()['server'],
        'photo': request.json()['photo'],
        'hash': request.json()['hash'],
        'group_id': vk_group_id
    }
    photo_id = api.photos.saveMessagesPhoto(**params)[0]['id']
    params = {
        'user_id': id,  # ID пользователя, которому мы должны отправить картинку
        'random_id': 0,
        'message': message,
        'attachment': f'photo-{vk_group_id}_{photo_id}'
    }
    api.messages.send(**params)
def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7)})

class VK:  # Подключаемся к VK
    def __init__(self, access_token, user_id, version='5.131'):
        self.token = access_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def get_users_info(self, id):
        url = vk_link + 'users.get'
        params = {'user_ids': self.id}
        response = requests.get(url, params={**self.params, **params})
        return response.json()

    def get_fotos(self, f_count, user_id, album='profile'):
        url = vk_link + 'photos.get'
        params = {'owner_id': user_id,
                  'album_id': album,
                  'extended': '1',
                  'photo_sizes': '1',
                  'count': f_count
                  }
        response = requests.get(url, params={**self.params, **params})
        return response.json()

    def search_users(self, age, sex, city):
        url = vk_link + 'users.search'
        if sex == 'ж':
            sex = 1
        elif sex == 'м':
            sex = 2
        else:
            sex = 0

        params = {'age_from': age,
                  'age_to': age,
                  'sex': sex,
                  'hometown': city,
                  'count': count_raw_search,
                  'has_photo': 1,
                  'fields': 'counters, screen_name',
                  }
        response = requests.get(url, params={**self.params, **params})
        return response.json()

    def vk_get_partners_photos(self, partners_info, album='profile'):
        url = vk_link + 'photos.get'
        raw_result = []
        for partner in partners_info:
            params = {'owner_id': partner['id'],
                      'album_id': album,
                      'extended': '1',
                      'photo_sizes': '1'
                      }
            response = requests.get(url, params={**self.params, **params})
            prom_result = response.json()

            raw_result.append({'partner_id': partner['id'], 'partner_photos': prom_result})
            sleep(1)


        return raw_result
    def vk_get_current_foto(self, id_partner, photos, album='profile' ):
        url = vk_link + 'photos.get'
        result = []
        for photo in photos:
            photo['response']['items']

            params = {'owner_id': photo['id'],
                      'album_id': album,
                      'extended': '1',
                      'photo_sizes': '1'
                      }
            response = requests.get(url, params={**self.params, **params})
            prom_result = response.json()
            sleep(1)
