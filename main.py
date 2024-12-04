import requests
from bs4 import BeautifulSoup
import json

# URL для парсинга
url = 'https://mgkct.minskedu.gov.by/%D0%BE-%D0%BA%D0%BE%D0%BB%D0%BB%D0%B5%D0%B4%D0%B6%D0%B5/%D0%BF%D0%B5%D0%B4%D0%B0%D0%B3%D0%BE%D0%B3%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9-%D0%BA%D0%BE%D0%BB%D0%BB%D0%B5%D0%BA%D1%82%D0%B8%D0%B2'

# Отправляем GET-запрос
response = requests.get(url)
if response.status_code != 200:
    print(f"Ошибка при запросе к сайту: {response.status_code}")
    exit()

soup = BeautifulSoup(response.text, 'html.parser')

# Находим все элементы с классом 'content taj'
teachers = soup.find_all('div', class_='content taj')

# Списки для преподавателей
list_teachers = []

# Заполняем списки данными
for teacher in teachers:
    name_tag = teacher.find('h3')
    post_tag = teacher.find('li', class_='tss')
    if name_tag and post_tag:
        name = name_tag.get_text(strip=True)
        post = post_tag.get_text(strip=True).replace('Должность: ', '')
        list_teachers.append({"Teacher": name, "Post": post})

# Проверка на наличие данных
if not list_teachers:
    print("Не удалось найти данные о преподавателях.")
else:
    # Выводим данные в требуемом формате
    for i, teacher in enumerate(list_teachers):
        print(f"{i + 1}. Teacher: {teacher['Teacher']}; Post: {teacher['Post']};")

    # Сохранение данных в файл data.json
    file_json = "data.json"
    print("Записываем данные в файл data.json")
    with open(file_json, "w", encoding='utf-8') as file:
        json.dump(list_teachers, file, indent=4, ensure_ascii=False)

    print("Проверяем содержимое файла data.json:")
    with open(file_json, "r", encoding='utf-8') as file:
        data = json.load(file)
        print(json.dumps(data, indent=4, ensure_ascii=False))

    # Генерация HTML файла на основе данных из data.json
    file_index = "index.html"

    with open(file_index, "w", encoding='utf-8') as file:
        file.write("""<html>
<head>
    <title>Teacher Information</title>
    <style>
        body {
            background-color: #f0f0f0;
            font-family: Arial, sans-serif;
        }
        h1 {
            text-align: center;
            color: #333;
        }
        table {
            border-collapse: collapse;
            width: 80%;
            margin: 20px auto;
            background-color: #fff;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #4CAF50;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
    </style>
</head>
<body>
    <h1>Teacher Information</h1>
    <table>
        <tr>
            <th>Teacher</th>
            <th>Post</th>
            <th>Number</th>
        </tr>
""")

        with open(file_json, "r", encoding='utf-8') as input_file:
            data_writer = json.load(input_file)
            for i, item in enumerate(data_writer):
                file.write(f"<tr><td>{item['Teacher']}</td><td>{item['Post']}</td><td>{i + 1}</td></tr>\n")

        file.write("""
    </table>
    <p style="text-align: center;"><a href="https://mgkct.minskedu.gov.by/">Источник данных</a></p>
</body>
</html>
""")

    print("HTML файл создан: index.html")
