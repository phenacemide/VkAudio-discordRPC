import time
import os

import requests
import vk_api

from pypresence import Presence
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


timestamp_start = int(time.time())


with open('tokens.txt', 'r', encoding='utf-8') as file:
    vktoken, vk_user_id, discord_app_id = [i.strip().split('=')[1] for i in file.readlines()]


session = vk_api.VkApi(token=vktoken)
vk = session.get_api()
rpc = Presence(discord_app_id)


def get_vk_user_status() -> bool | tuple:
    status = vk.users.get(user_id=vk_user_id, fields='status')
    try:
        status = status[0]['status_audio']
    except IndexError and KeyError:
        return False

    current_audio = status['artist'], status['title']
    return current_audio


def get_audio_image(image_name: str) -> str:
    """
    Функция через которую получаем ссылку на картинку текущего аудио
    """
    try:
        headers = {
            'user-agent': UserAgent().random
        }

        html = requests.get(f'https://www.google.com/search?q={image_name.replace(" ", "%")}&tbm=isch', headers=headers)
        soup = BeautifulSoup(html.text, 'lxml')
        images = soup.find_all("img")
        img = images[1].get('src')
        return img
    except Exception as ex:

        print(ex)
        return '6f042f6867a06a513653ca0131f9f61e'


def stream_music_to_discord(count: int = 3):

    if not (status := get_vk_user_status()):
        if not count:
            print(f"\bАудио так и не было найдено, попробуем повторно подключиться через 2.5 минут")
            time.sleep(150)

        for i in range(5, 0, -1):
            print(f"\bАудио не производится, презапуск через {i} секунд")
            time.sleep(1)

        rpc.clear()
        os.system('cls')

        stream_music_to_discord(count=count-1)

    artist = f"{status[0]}"
    track = f"{status[-1]}"
    image = get_audio_image(f"{track} {artist}")

    print(f"Current Track: {artist} - {track}")

    rpc.update(
        start=timestamp_start,
        large_image=image,
        small_image=image,
        state=artist,
        details=track,
    )

    time.sleep(30)
    stream_music_to_discord()


if __name__ == '__main__':
    while 1:
        print('Conecting...')
        rpc.connect()
        stream_music_to_discord()
