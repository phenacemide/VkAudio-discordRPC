<div align="center"><a>🔴 Only Ru Readme, because vk is a russian social network!</a></div>

# VkAudio-DiscordRPC
## Script which getting current audio from vk user page with api and stream it to discord RPC

____
### 🏁 Начинаем

- Для того чтобы наш скрипт РАБОТАЛ, нам нужно создать два приложения и достать их токены

  **ВК**:

    - Переходим на [сайт](https://vk.com/editapp?act=create) и создаем Standalone приложение с любым названием
    <p align="center"><img src="https://cdn.discordapp.com/attachments/1042826853372674190/1047171950813925468/image.png" alt="vk"/></p>


    - Переходим вот [сюда](https://vk.com/apps?act=manage)  и нажимаем редактировать на созданное приложение и копируем сервисный ключ:
    <p align="center"><img src="https://cdn.discordapp.com/attachments/1042826853372674190/1047174360735154246/image.png" alt="vk"/></p>

  **Дискорд**:

    - Создаём [тут](https://discord.com/developers/applications/) приложение (Тут уже можете сделать название)
    <p align="center"><img src="https://cdn.discordapp.com/attachments/1042826853372674190/1047177303156854834/image.png" alt="ds"/></p>


    - Переходим в созданное вами приложение и копируем Application ID


  **Редактируем tokens.txt**

    - Если вы скачивали exe [отсюда](https://github.com/gentoumashiro/VkAudio-discordRPC/releases/download/release/DiscordRPC.exe), то необходимо возле скачанного файла создать текстовый файл с именем (**ВАЖНО**): tokens.txt 
    - Открываем наш файл **tokens.txt** и вставляем туда вот такие слова:
    <p align="center"><img src="https://cdn.discordapp.com/attachments/1042826853372674190/1047180071577858139/image.png" alt="tokens"/><p>

    **БЕЗ ЗВЁЗДОЧЕК И ЧТОБЫ В ФАЙЛЕ БЫЛО РОВНО 3 СТРОКИ**

  **Если всё сделали верно то будет такой вот результат**:
  <p align="center"><img src="https://cdn.discordapp.com/attachments/1042826853372674190/1047853889921224705/image.png" alt="result"/><p>    
  <p align="center"><img src="https://cdn.discordapp.com/attachments/1042826853372674190/1047853938721951835/image.png" alt="result"/><p>    
  

### Теперь гайд для тех кто хочет сам скомпилировать код и/или запускать именно скрипт

  - git clone https://github.com/gentoumashiro/VkAudio-discordRPC.git
  - cd VkAudio-discordRPC
  - python -m venv venv
  - venv\scripts\activate
  - pip install -r requirements.txt
  
____
**Всё готово, осталось лишь добавить файл tokens.txt рядом с main.py и вписать туда свои значения**

    -Если хотите скомпилировать файл в один exe, то:

      -pip install pyinstaller
      -pyinstaller --onefile --noconfirm --console -n DiscordRPC "укажите полный путь до \main.py"
      -готовая версия будет лежать в папке dist. Не забудьте добавить сюда tokens.txt

P.S. Также вы можете добавить exe файл в Windows Services чтобы exe тихо запускался при старте системы

### ✍️ Authors: 
**phenacemide#2436**
