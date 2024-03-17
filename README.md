# Minecraft Bioms Checker Telegram Bot
___
# RU :ru:

## Описание
![adventuring_time_logo](https://private-user-images.githubusercontent.com/116081113/313502647-3ce53ae5-339c-49e9-a0c5-89c938338589.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MTA3MDc1NzcsIm5iZiI6MTcxMDcwNzI3NywicGF0aCI6Ii8xMTYwODExMTMvMzEzNTAyNjQ3LTNjZTUzYWU1LTMzOWMtNDllOS1hMGM1LTg5YzkzODMzODU4OS5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjQwMzE3JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI0MDMxN1QyMDI3NTdaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT1jNjkyZTllZGE1ZDYwZTFhYjdkMDg3MTQzYjExYTczYTc4OTZmMjA2YTM1MzFlMGVhYmQzZjMyYTYwNDM0NzVjJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZhY3Rvcl9pZD0wJmtleV9pZD0wJnJlcG9faWQ9MCJ9.ji2HxvTUYOMw2rgRAgNXl8MzcDf7xPb0xoFJxAkNJ4M)

Данный телеграм-бот помогает найти ненайденные биомы и составить статистику по биомам, чтобы 
быстро и легко выполнить достижение __Adventuring Time__. 
Tелеграм-бот позволяет загружать эталоны разных версий, которые будут сравниваться с пользовательскими картами.
Пользователь сможет загружать множество карт и смотреть прогресс по ним с помощью удобного интерфейса в виде меню карт
и передвигаться по нему с помощью inline-кнопок.





___


## Используемый софт
Бот работает на __python3.12__ и написан на библиотеке [Aiogram](https://aiogram.dev).
Для реализации кэша используется нереляционная БД [Redis](https://redis.io). Для удобного запуска на хосте используется
[Docker](https://www.docker.com), в котором развернуто 2 контейнера с логикой бота, а также redis-сервером.
Используется кастомный образ на основе `python:3.12.2-alpine3.19` и стоковый образ redis - `redis:latest`.
___

## Возможности бота

* Добавление эталонных карт для поддержки различных версий (данное действие может выполнить только __админ__);
* Добавление неограниченного количества карт, которые закрепляются к пользователю;
* Просмотр прогресса по нужной карте:
  * Количество найденных биомов;
  * Количество ненайденных биомов;
  * Шкала прогресса с процентами;
  * Список найденных и ненайденных биомов соответственно;
___

## Настройка перед запуском
После скачивания исходного кода нужно настроить работу бота.
### Создание телеграм-бота
Для работы бота потребуется токен, который нужно получить от телеграма. Он выдается после создания бота.
В телеграме для этого используется [Bot Father](https://telegram.me/BotFather).
### Настройка переменных окружения
После того как вы получили свой уникальный токен, его нужно сохранить в безопасном месте.
Для этого создаем файл `.env` в корне проекта и помещаем туда переменную `TELEGRAM_TOKEN`.
Должно получиться так:
```python
# .env
TELEGRAM_TOKEN=some_token123
```
> Также вы можете добавить свои переменные окружения, если потребуется. Все переменные попадут в образ __alpine__.
### Добавление администраторов
Для того чтобы была возможность добавлять или удалять эталоны карт, требуется добавить администраторов.
Их __telegram id__ в виде строки требуется прописать в множество `ADMIN_ID_SET` в файл `settings.py`.
Чтобы узнать свой __telegram id__ можно использовать [этого бота](https://t.me/getmyid_bot).
### Опциональный настойки
Вы также можете изменить название таблиц БД, логов и другое, изменяя соответствующие имена в `setting.py`.
___
## Запуск бота
Теперь можно перейти к самому интересному:grinning:. Чтобы, запустить бота потребуется открыть терминал и прописать
следующие команды:
```bash
cd #путь до корневой директории проекта
docker compose up
```
Первая команда сделает данную директорию рабочей, вторая - запустит процесс сборки двух контейнеров.
После сборки контейнеры начнут работать, и можно увидеть первые логи в консоле:
```
bot_logger [DEBUG] -- xx-xx-xxxx xx:xx:xx -- Bot started
```
Теперь можно начать пользоваться ботом!

---
## Использование бота
Бот принимает следующие команды:
* /start - начало диалога;
* /help - помощь по боту;
* /add_map - добавление карты;
* /map_list - список доступных карт у пользователя;
* /delete_map - удаления карты;
* /add_advancement - добавления эталона карты (Только для администраторов);
* /delete_advancement - удаления эталона карты (Только для администраторов);

![menu](https://private-user-images.githubusercontent.com/116081113/313502665-3cbfdb6a-4eaf-4bd9-9552-4c7b08aeffb6.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MTA3MDc1NzcsIm5iZiI6MTcxMDcwNzI3NywicGF0aCI6Ii8xMTYwODExMTMvMzEzNTAyNjY1LTNjYmZkYjZhLTRlYWYtNGJkOS05NTUyLTRjN2IwOGFlZmZiNi5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjQwMzE3JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI0MDMxN1QyMDI3NTdaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT1jYmMyNjUzZGVhMjE2MWU4NmZlZjkxYzc5YjRlN2I2ZmNmNDVhZDM2OGI1OGFkYjhkNjAxNGIxOTIzMzc5OGNkJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZhY3Rvcl9pZD0wJmtleV9pZD0wJnJlcG9faWQ9MCJ9.O0B1Vcf_kdGWsTQc_xrZqG86Wl-H2Tdds1xM5u2FGSM)


<img src="https://private-user-images.githubusercontent.com/116081113/313502658-17ff8208-6a31-42e7-8990-0aae7f9e74a8.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MTA3MDc1NzcsIm5iZiI6MTcxMDcwNzI3NywicGF0aCI6Ii8xMTYwODExMTMvMzEzNTAyNjU4LTE3ZmY4MjA4LTZhMzEtNDJlNy04OTkwLTBhYWU3ZjllNzRhOC5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjQwMzE3JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI0MDMxN1QyMDI3NTdaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT1iOGI0MTJiNmYzOTA4MWM2YjA5NTVlMmFkZTY2YWU2OGVmODhiYjViMGNmYjA3NzA0NTE4NWQwMTA1ZWUxNmQ1JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZhY3Rvcl9pZD0wJmtleV9pZD0wJnJlcG9faWQ9MCJ9.zO2QI2T22j_Pft3gUox1r4xhxN0lZecOP8dDfEaMgJc" width="285" height="800">

---

# Minecraft Bioms Checker Telegram Bot
___
# EN :us:

## Description
![adventuring_time_logo](https://private-user-images.githubusercontent.com/116081113/313502647-3ce53ae5-339c-49e9-a0c5-89c938338589.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MTA3MDc1NzcsIm5iZiI6MTcxMDcwNzI3NywicGF0aCI6Ii8xMTYwODExMTMvMzEzNTAyNjQ3LTNjZTUzYWU1LTMzOWMtNDllOS1hMGM1LTg5YzkzODMzODU4OS5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjQwMzE3JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI0MDMxN1QyMDI3NTdaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT1jNjkyZTllZGE1ZDYwZTFhYjdkMDg3MTQzYjExYTczYTc4OTZmMjA2YTM1MzFlMGVhYmQzZjMyYTYwNDM0NzVjJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZhY3Rvcl9pZD0wJmtleV9pZD0wJnJlcG9faWQ9MCJ9.ji2HxvTUYOMw2rgRAgNXl8MzcDf7xPb0xoFJxAkNJ4M)

This Telegram bot helps to find undiscovered biomes and compile statistics on biomes to quickly and easily achieve the __Adventuring Time__ achievement. The Telegram bot allows uploading templates of different versions that will be compared with user maps. Users can upload multiple maps and track their progress using a convenient menu interface and navigate through it using inline buttons.

___

## Used Software
The bot runs on __python3.12__ and is written using the [Aiogram](https://aiogram.dev) library. Non-relational database [Redis](https://redis.io) is used for cache implementation. For convenient hosting, [Docker](https://www.docker.com) is used, where 2 containers with bot logic and a Redis server are deployed. It uses a custom image based on `python:3.12.2-alpine3.19` and the stock Redis image - `redis:latest`.
___

## Bot's Capabilities

* Adding template maps to support different versions (only the __admin__ can perform this action);
* Adding an unlimited number of maps assigned to the user;
* Viewing progress on the desired map:
  * Number of found biomes;
  * Number of undiscovered biomes;
  * Progress bar with percentages;
  * Lists of found and undiscovered biomes respectively;
___

## Configuration before Running
After downloading the source code, you need to configure the bot's operation.

### Creating a Telegram Bot
To work with the bot, you will need a token obtained from Telegram. It is issued after creating the bot. In Telegram, this is done using [Bot Father](https://telegram.me/BotFather).

### Setting Environment Variables
After you have obtained your unique token, you need to save it in a secure place. To do this, create a `.env` file in the project's root and place the `TELEGRAM_TOKEN` variable there. It should look like this:
```python
# .env
TELEGRAM_TOKEN=some_token123
```
> You can also add your own environment variables if needed. All variables will be included in the __Alpine__ image.

### Adding Administrators
To have the ability to add or delete map templates, administrators need to be added. Their __telegram id__ in the form of a string needs to be added to the `ADMIN_ID_SET` set in the `settings.py` file.
To find out your __Telegram ID__, you can use [this bot](https://t.me/getmyid_bot).

### Optional Settings
You can also change the names of database tables, logs, and more by changing the corresponding names in `setting.py`.
___

## Running the Bot
Now you can move on to the most interesting part 😄. To start the bot, open the terminal and enter the following commands:
```bash
cd #path_to_project_root_directory
docker compose up
```
The first command sets this directory as the working directory, and the second command starts the process of building two containers. After building the containers, they will start working, and you can see the first logs in the console:
```
bot_logger [DEBUG] -- xx-xx-xxxx xx:xx:xx -- Bot started
```
Now you can start using the bot!
___
## Using the Bot
The bot accepts the following commands:
* /start - start of the dialog;
* /help - help with the bot;
* /add_map - adding a map;
* /map_list - list of available maps for the user;
* /delete_map - deleting a map;
* /add_advancement - adding a map template (Only for administrators);
* /delete_advancement - deleting a map template (Only for administrators);

---