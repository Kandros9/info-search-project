import requests
from bs4 import BeautifulSoup
import time
from src.constants import DOMAIN


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


def get_doc_num(page_num):
    return str(page_num).zfill(3)


def get_pages(url, max_pages=100):
    html_doc = requests.get(url)
    soup = BeautifulSoup(html_doc.text, "html.parser")
    page_num = 1
    print("Found links:")
    with open('data/index.txt', 'w') as file:
        for link in soup.find_all('a'):
            if accept_link(link):
                url = DOMAIN + link['href']
                doc_num = get_doc_num(page_num)
                dump_page(doc_num, url)
                file.write('%s:%s\n' % (doc_num, url))
                page_num += 1
                print(url)
            if page_num > max_pages:
                print("Total count: " + str(page_num - 1))
                break


def read_doc(page_num):
    with open('../pages/' + get_doc_num(page_num) + '.html', 'r', encoding='utf-8') as dump_file:
        soup_dump = BeautifulSoup(dump_file.read(), "html.parser")
    return soup_dump


def get_doc_text(soup):
    # remove all script and style elements
    for script in soup(["script", "style"]):
        script.extract()

    text = soup.get_text()

    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text
