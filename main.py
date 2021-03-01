import requests
from bs4 import BeautifulSoup
from sys import argv
import time

script_name, first = argv
MAX_PAGES = int(first)
DOMAIN = 'https://en.wikipedia.org'


def accept_link(link):
    return link.has_attr('href') \
           and link.has_attr('title') \
           and not link.has_attr('class') \
           and link['href'].split('/')[1] == 'wiki' \
           and ':' not in link['href'] \
           and '#' not in link['href']


def dump_page(doc_num, url):
    with open('pages/' + doc_num + '.html', 'w', encoding='utf-8') as dump_file:
        html_doc_dump = requests.get(url)
        soup_dump = BeautifulSoup(html_doc_dump.text, "html.parser")
        dump_file.writelines(str(soup_dump))
    time.sleep(5)


def get_page_links(url):
    html_doc = requests.get(url)
    soup = BeautifulSoup(html_doc.text, "html.parser")
    page_num = 1
    print("Found links:")
    with open('index.txt', 'w') as file:
        for link in soup.find_all('a'):
            if accept_link(link):
                url = DOMAIN + link['href']
                doc_num = str(page_num).zfill(3)
                dump_page(doc_num, url)
                file.write('%s:%s\n' % (doc_num, url))
                page_num += 1
                print(url)
            if page_num > MAX_PAGES:
                print("Total count: " + str(page_num - 1))
                break


# There are about 1000 links that satisfy on this page
get_page_links(DOMAIN + '/wiki/Astronomy')
