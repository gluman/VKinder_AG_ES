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


