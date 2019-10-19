# Источник https://geekbrains.ru/posts
# Задача:
# Необходимо обойти все записи блога и получить следующую структуру информации:
#
# {
# "title": заголовок статьи,
# "image": Заглавное изображение статьи (ссылка),
# "text": Текст статьи,
# "pub_date": time_stamp даты публикации,
# "author": {"name": Имя автора,
#                "url": ссылка на профиль автора,
#                },
# }
# по окончанию сбора, полученые данные должны быть сохранены в json файл.
# В структуре должны присутсвовать все статьи на дату парсинга

import requests
from datetime import datetime as dt
from bs4 import BeautifulSoup
import json

domain_url = 'https://geekbrains.ru'
blog_url = 'https://geekbrains.ru/posts'

def month_string_to_timestamp(string): # перевод текстовой даты в timestamp
    m = {
        'янв':'01',
        'фев':'02',
        'мар':'03',
        'апр':'04',
        'мая':'05',
        'июн':'06',
        'июл':'07',
        'авг':'08',
        'сен':'09',
        'окт':'10',
        'ноя':'11',
        'дек':'12'
        }
    s = string.strip()[3:6].lower()

    try:
        out = m[s]
        date = f'{string[:2]}{out}{string[-4:]}'
        date_format = dt.strptime(date, "%d%m%Y")
        return dt.timestamp(date_format)
    except KeyError:
        print('Not a month')

def get_soup(url): # создаем Soup
    page_data = requests.get(url)
    soup_data = BeautifulSoup(page_data.text, 'lxml')
    return soup_data

problem_url = [] # контейнер для url на которых не собираются картинки

def get_image(post_data_post_url, url, post): # собираем картинки в публикациях
    try:
        image = post_data_post_url.find('div', class_='blogpost-content').find('img').attrs['src']
    except AttributeError:
        link = post.find('a').attrs.get('href')
        image = get_soup(url).find('a', attrs={'href': link}).find('img').attrs.get('src')
    except:
        problem_url.append(link)
        image = 'No image'
    return image

def get_page_info(soup, url): # собираем информацию по заданию из каждой публикации
    page_posts_list = []
    posts_data_blog_url = soup.find_all('div', class_='post-item')

    for post in posts_data_blog_url:
        post_url = f"{domain_url}{post.find('a').attrs.get('href')}"
        post_data_post_url = get_soup(post_url).find('article', class_='col-sm-6 col-md-8 blogpost__article-wrapper')

        post_dict = {
            'title': post_data_post_url.find('h1').text,
            'image': get_image(post_data_post_url, url, post),
            'text': post_data_post_url.find('div', class_='blogpost-content').text,
            'pub_date': month_string_to_timestamp(post_data_post_url.find('time', class_='text-md').text),
            'author': {
                "name": post_data_post_url.find('div', class_='text-lg text-dark').text,
                "url": f"{domain_url}{post_data_post_url.find('div', class_='col-md-5').contents[0].get('href')}"
            },
        }

        page_posts_list.append(post_dict)
    return page_posts_list

def parcer(url): # собираем информацию по заданию из каждой публикации каждой страницы
    posts_list = []
    while True:
        soup = get_soup(url)
        posts_list.extend(get_page_info(soup, url))
        try:
            url = soup.find('a', attrs={'rel': 'next'}, text='›').attrs.get('href')
        except AttributeError:
            break
        url = f"{domain_url}{soup.find('a', attrs={'rel': 'next'}, text='›').attrs.get('href')}"
    return posts_list

result_data = parcer(blog_url)

with open(f'C:\\Users\\alber\\PycharmProjects\\GB_Basics\\result_data_BS_GB_{str(dt.now().date())}.json','w') as j_file:
    j_file.write(json.dumps(result_data))