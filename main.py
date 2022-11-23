import time
import os

import requests
import vk_api
import DiscordRPC

from bs4 import BeautifulSoup


"""
vktoken must be a string, like 'b1238zxclas1289zxlasdkas9asd'
vk_user_id can be string or int like 'llasllsldlsld' or 546823952
discord_app_id should be int like 123984205723952
"""

vktoken = ''
vk_user_id = ''  # если используешь цифровой id То удали ковычки
discord_app_id = None


session = vk_api.VkApi(token=vktoken)
vk = session.get_api()
rpc = DiscordRPC.RPC.Set_ID(app_id=discord_app_id)


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
    html = requests.get(f'https://www.google.com/search?q={image_name.replace(" ", "%")}&tbm=isch')
    soup = BeautifulSoup(html.text, 'lxml')
    images = soup.find_all("img")
    img = images[1].get('src')
    return img


def stream_music_to_discord(count: int = 3):

    if not (status := get_vk_user_status()):
        if not count:
            print(f"\033[91m\bАудио так и не было найдено, попробуем повторно подключиться через 5 минут")
            time.sleep(300)
            stream_music_to_discord()

        for i in range(5, 0, -1):
            print(f"\033[93m\bАудио не производится, презапуск через {i} секунд")
            time.sleep(1)

        os.system('cls')
        stream_music_to_discord(count=count-1)

    track = f"{status[-1]}"
    artist = f"{status[0]}"
    image = get_audio_image(f"{track} {artist}")

    print(f'\033[92mCurrent Track: {artist} - {track}')

    rpc.set_activity(
        large_image=image,
        small_image=image,
        state=artist,
        details=track,

    )
    time.sleep(30)
    stream_music_to_discord()


if __name__ == '__main__':
    stream_music_to_discord()
