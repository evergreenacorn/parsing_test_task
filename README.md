# Парсер для тестового задания

## Тестовое задание
Используя yml-фид из архива, вывести на консоль объекты категорий (всех) и офферов (первые 1000)

при этом картинки 1000 офферов должны быть скачены (асинхронно, в 10 тредов) в /tmp/<somedir>, после парсинга и скачивания в объекте оффера должен быть дополнен ключ
'file_path': '/tmp/<somedir>/<offer_id>.jpg'

технологии
lxml / asyncio / requests

## Что сделал:

1. Вывод на печать всех объетов категорий
2. Вывод на печать первых тысячи офферов
3. Скачивание картинок в /app/tmp/somdir посредством asyncio + threading (в 10 потоках, каждый со своим event_loop)
4. Логирование нескачавшихся картинок в /app/logs
5. После скачивания возвращаю словарь {'offer_key': {'file_path': 'local_file_path'}}, где offer_key - id объекта offer'а; file_path - полный путь картинки оффера, с данными которого, перезаписывается текущий файл .yml
6. Добавил docker-compose контейнер

## Как запустить:
1. docker-compose run parser_script
2. Выбрать нужный пункт меню от 0 до 4

## Что осталось сделать:
**TODO: {12.08.21}**
- [x] Слоты - только в классах парсера. Класс конфигурации - выдает отрицательный рост производительности или я что-то делаю не так...
- [ ] Разобраться с await - возвращаемыми значениями футуры - ругается на NoneType
- [ ] Тесты? - если нужно


## Библиотеки, которые использовал:
|Библиотека|Версия|
|:--|--:|
|asyncio|3.4.3|
|lxml|4.6.3|
|requests|2.26.0|
