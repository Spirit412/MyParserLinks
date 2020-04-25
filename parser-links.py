from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests
import lxml

DOMAIN = 'euroclimate.org'  # сайт для парсинга
HOST = 'https://' + DOMAIN
FORBIDDEN_PREFIXES = ['#', 'tel:', 'mailto:']
links = set()  # множество всех ссылок
# подсовываем данные браузера, имитируя запрос от браузера.
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
response = requests.get(HOST, headers=headers)


def add_all_links_recursive(url, maxdepth=5):
    print('{:>5}'.format(len(links)), url[len(HOST):])

    # глубина рекурсии не более `maxdepth`

    # список ссылок, от которых в конце мы рекурсивно запустимся
    links_to_handle_recursive = []
    # получаем html код страницы
    request = requests.get(url, headers=headers)
    # парсим его с помощью BeautifulSoup
    soup = BeautifulSoup(request.content, 'lxml')
    # рассматриваем все теги <a>

    for tag_a in soup.find_all('a', href=lambda v: v is not None):
        link = tag_a['href']

        # если ссылка не начинается с одного из запрещённых префиксов
        if all(not link.startswith(prefix) for prefix in FORBIDDEN_PREFIXES):
            # проверяем, является ли ссылка относительной
            # например, `/oplata` --- это относительная ссылка
            # `http://101-rosa.ru/oplata` --- это абсолютная ссылка
            if link.startswith('/') and not link.startswith('//'):
                # преобразуем относительную ссылку в абсолютную
                link = HOST + link
            # проверяем, что ссылка ведёт на нужный домен
            # и что мы ещё не обрабатывали такую ссылку
            if urlparse(link).netloc == DOMAIN and link not in links:
                links.add(link)
                links_to_handle_recursive.append(link)

    if maxdepth > 0:
        for link in links_to_handle_recursive:
            add_all_links_recursive(link, maxdepth=maxdepth - 1)


def main():
    add_all_links_recursive(HOST + '/')
    for link in links:
        print(link)


if __name__ == '__main__':
    main()
