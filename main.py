import os
import time

import requests
import vk_api

from bs4 import BeautifulSoup
from pypresence import Presence


image = ['6f042f6867a06a513653ca0131f9f61e']


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
    и заменяем единственный элемент в списке Image На найденную картинку,
    Если же функция не сможет найти изображение, то используем прдыдущую картинку
    """
    global image

    try:
        req = requests.get(f'https://www.google.com/search?q={image_name.replace(" ", "%")}&tbm=isch')
        soup = BeautifulSoup(req.text, 'xml')
        images = soup.find_all("img")
        image[0] = images[1].get('src')
        return image[0]
    except Exception as exx:
        print(f"Ошибка: {exx}")
        return image[0]


def stream_music_to_discord(timestamp: int = int(time.time()), count: int = 3):
    if not (status := get_vk_user_status()):
        if not count:
            print(f"\bАудио так и не было найдено, попробуем повторно подключиться через 2.5 минут")
            time.sleep(150)
            count = 3
        for i in range(5, 0, -1):
            print(f"\bАудио не производится, презапуск через {i} секунд")
            time.sleep(1)
        os.system('cls')
        stream_music_to_discord(count=count - 1)

    artist = f"{status[0]}   "
    track = f"{status[-1]}   "
    current_track = f"{artist.strip()} - {track.strip()}"
    img = get_audio_image(f"{track} {artist}")

    print(f"Current Track: {current_track}")

    rpc.update(
        state=artist,
        details=track,
        start=timestamp,
        large_image=img,
        large_text=current_track,
        small_image=img,
        small_text=artist,
    )

    time.sleep(15)
    os.system('cls')
    stream_music_to_discord(count=3)


def main():
    try:
        print('Conecting to discord...')
        rpc.connect()
        timestamp_start = int(time.time())
        stream_music_to_discord(timestamp_start)
    except Exception as ex:
        print(F"Ошибка: {ex} !!!")
        print(F"Попробуйте запустить дискорд или запустить exe от имени администратора!!\nПерезапуск через 10 секунд!!")
        time.sleep(10)
        main()


if __name__ == '__main__':
    main()
