from random import randrange

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from Settings import VK_TOKEN

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


    def get_user_vkinfo(id):
        pass

