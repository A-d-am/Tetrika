import requests
from bs4 import BeautifulSoup

url = "https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%96%D0%B8%D0%B2%D0%BE%D1%82%D0%BD%D1%8B%D0%B5_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83"
page = requests.get(url).text  # ответ сервера (его содержимое)
data = []
alphabet = [
    'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х',
    'Ц', 'Ч', 'Ш', 'Щ', 'Э', 'Ю', 'Я']

flag = True
while flag:
    soup = BeautifulSoup(page, 'lxml')
    names = soup.find('div', class_='mw-category').find_all(
        'li')  # ищем в коде страницы такой div, а в нем ищем все теги <li>
    for name in names:  # перебираем все названия, и записываем в список data для дальнейшей их обработки
        if name.text[0] == 'A':  # здесь идет проверка на язык алфавита ( т.к. А здесь из английского алфавита)
            flag = False
            break
        else:
            data.append(name.text)
    links = soup.find('div', class_="mw-content-ltr").find_all('a')  # ищем ссылку для перехода на след страницу
    for a in links:
        if a.text == 'Следующая страница':
            url = 'https://ru.wikipedia.org/' + a.get('href')
            page = requests.get(url).text

count = 0
for b in alphabet:  # этот цикл переребирает каждую букву из списка alphabet и считает, сколько слов на нее начинается
    for a in data:
        if b == a[0]:
            count += 1
    print(f'{b}:{count}')
    count = 0
# для удобвства провеки ниже дан результат работы этой программы
# А:1091
# Б:1505
# В:488
# Г:935
# Д:707
# Е:99
# Ё:2
# Ж:381
# З:584
# И:327
# Й:3
# К:2078
# Л:665
# М:1185
# Н:431
# О:731
# П:1646
# Р:528
# С:1663
# Т:913
# У:230
# Ф:172
# Х:253
# Ц:206
# Ч:628
# Ш:259
# Щ:141
# Э:195
# Ю:124
# Я:196
