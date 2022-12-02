import os
import time

import requests
import vk_api

from urllib.parse import quote
from bs4 import BeautifulSoup
from pypresence import Presence


image = ['6f042f6867a06a513653ca0131f9f61e']
timestamp = int(time.time())


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

    current_audio_details = status['artist']+'   ', status['title']+'   '
    return current_audio_details


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
    except IndexError:
        return image[0]


def get_current_track_link(track_name: str):
    track_link = 'https://www.youtube.com/results?search_query='+quote(f"{track_name}")
    return track_link


def get_audio_details(audio_details: tuple):
    artist, track = audio_details
    audio_name = f"{artist.strip()} - {track.strip()}"
    audio_link = get_current_track_link(audio_name)
    img = get_audio_image(f"{track} {artist}")
    return artist, track, audio_name, audio_link, img


def stream_music_to_discord(audio_details: tuple):

    artist, track, audio_name, audio_link, img = get_audio_details(audio_details)
    print(f'Current Track: {audio_name}')

    rpc.update(
        state=artist,
        details=track,
        start=timestamp,
        large_image=img,
        large_text=audio_name,
        small_image=img,
        small_text=artist,
        buttons=[
            {
                "label": f"{audio_name[:32]}",
                "url": audio_link,
            }
        ]
    )


def main():
    count = 3
    while True:
        if not (status := get_vk_user_status()):
            if not count:
                print(f"Аудио так и не было найдено, попробуем через 3 минуты")
                time.sleep(180)
                main()
            os.system('cls')
            for i in range(4, 0, -1):
                print(f"Аудио не производится, презапуск через {i} секунд")
                time.sleep(1)
            count -= 1
            continue
        stream_music_to_discord(status)
        time.sleep(15)
        main()


if __name__ == '__main__':
    try:
        print('Conecting to discord...')
        rpc.connect()
        main()
    except Exception as ex:
        print(F"Ошибка: {ex}")
        time.sleep(10)
        os.system('cls')
