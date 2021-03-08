from sys import argv
from src.crawler import get_pages
from src.constants import DOMAIN

MAX_PAGES = argv[1] if len(argv) > 1 else 100
SECTION = argv[2] if len(argv) > 2 else 'Astronomy'

get_pages(DOMAIN + '/wiki/' + SECTION, int(MAX_PAGES))
