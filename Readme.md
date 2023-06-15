<h2 style='font-size: 30px !important;'>PARSER HH.RU</h2>
<div><span style='font-weight: bold'>Parser hh.ru</span> - программное обеспечение, позволяющее извлекать данные по вакансиям и резюме с сайта hh.ru и предоставлять статистику на основе полученных данных.</div>
<h2 style='font-size: 30px !important;'>Установка библиотек</h2>

```pip install -r ./requirements.txt```
<h2 style='font-size: 30px !important;'>Запуск программы</h2>

```py ./gui.py```

<h2 style='font-size: 30px !important;'>Демонстрация работы</h2>
<li>Начальное окно</li><br>

![Alt text](https://i.yapx.cc/WJ6on.png)

<li>Авторизация в ЛК через Selenuim</li><br>

![Alt text](https://i.postimg.cc/7Y4g50nK/image.png)

![Alt text](https://i.yapx.ru/WJ6uJ.png)

<li>Выбор парсинга</li><br>

![Alt text](https://i.yapx.ru/WJ6uX.png)

<li>Работа с вакансиями</li>
<div>Пользователь обязательно должен ввести <span style='font-weight: bold'>название вакансии</span> и ввести <span style='font-weight: bold'>количество страниц</span> для парсинга, с которых будут взяты вакансии<span style='font-weight: bold'> (1 страница = 20 вакансии)</span>. Остальные настройки поиска пользователь указывает на свое усмотрение.</div>

![Alt text](https://i.yapx.ru/WJ6u5.png)

<li>Статистика по вакансиям</li>
<div>Статистика получается на основе полученных ранее спаршенных данных.</div>

![Alt text](https://i.yapx.ru/WJ6vY.png)
![Alt text](https://i.yapx.ru/WJ6v9.png)

<li>Отклик на вакансию(и)</li>
<div>Пользователю необходимо выбрать нужное резюме и интересующую вакансию, написав при этом сопроводительное письмо, если требуется. Состояние отклика видно в нижнем окне.</div>

![Alt text](https://i.yapx.ru/WJ6wg.png)

<li>Работа с резюме</li>
<div>Пользователь обязательно должен ввести <span style='font-weight: bold'>название резюме</span> и ввести <span style='font-weight: bold'>количество страниц</span> для парсинга, с которых будут взяты резюме<span style='font-weight: bold'> (1 страница = 20 резюме)</span>. Остальные настройки поиска пользователь указывает на свое усмотрение.</div>

![Alt text](https://i.yapx.ru/WJ6wu.png)

<li>Статистика по резюме</li>
<div>Статистика получается на основе полученных ранее спаршенных данных.</div>

![Alt text](https://i.yapx.ru/WJ6yB.png)
![Alt text](https://i.yapx.ru/WJ6yH.png)

<li>Автосохрание данных</li>
<div>После парсинга данных происходит автосохранение данных в CSV-файл директории проекта.</div>

![Alt text](https://im.wampi.ru/2023/06/15/image694bbaf5590e1c37.png)