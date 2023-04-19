from random import randrange
import requests
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from Settings import VK_TOKEN, base_vk_link as vk_link

# token = input('Token: ')
token = VK_TOKEN


vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)



def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})

class VK_SEARCH:  # Подключаемся к VK
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

    def serach_users(self, age, sex, city):
        url = vk_link + 'users.get'
        params = {'user_ids': self.id}

