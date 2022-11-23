import time
import os

import vk_api
import DiscordRPC

"""
vktoken must be a string, like 'b1238zxclas1289zxlasdkas9asd'
vk_user_id can be string or int like 'llasllsldlsld' or 546823952
discord_app_id should be int like 123984205723952
large_image should be URI or the key received in the discord application
"""

vktoken = ''
vk_user_id = ''  # если используешь цифровой id То удали ковычки
discord_app_id = None
large_image = '6f042f6867a06a513653ca0131f9f61e'


session = vk_api.VkApi(token=vktoken)
vk = session.get_api()
rpc = DiscordRPC.RPC.Set_ID(app_id=discord_app_id)


def get_vk_user_status() -> bool | tuple:
    status = vk.users.get(user_id=vk_user_id, fields='status')
    try:
        status = status[0]['status_audio']
    except:
        return False

    current_audio = status['artist'], status['title']
    return current_audio


audio = get_vk_user_status()


def check_audio(func):
    """
    Функция, которая проверяет наличие аудиозаписи в статусе вк,
    в случае, если аудиозаписи нет в статусе - перезапускает функцию
    :param func:
    :return:
    """
    def wrapper(status=audio, count: int = 3):
        if not status:
            if not count:
                print(f"Аудио так и не было найдено, попробуем повторно подключиться через 5 минут")
                time.sleep(300)
                func()
            for i in range(5, 0, -1):
                print(f"Аудио не производится, презапуск через {i} секунд")
                time.sleep(1)
            os.system('cls')
            count -= 1
            func(count)
        func()
    return wrapper


@check_audio
def stream_music_to_discord():
    current_track = get_vk_user_status()

    track = f"{current_track[-1]}"
    artist = f"by {current_track[0]}"

    print(f"Текущий трек: {artist} - {track}")

    rpc.set_activity(
        large_image=large_image,
        state=artist,
        details=track,
        timestamp=time.time()
    )
    time.sleep(60)
    stream_music_to_discord()


if __name__ == '__main__':
    stream_music_to_discord()
