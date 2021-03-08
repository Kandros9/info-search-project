# Info search semester project, ITIS 2021

Student: Evelina Ravilova

## Features

##### Web crawler
  Get pages from Wikipedia articles (branch `feature/web-crawler`)
  
##### Preprocessing
  Tokenize and lemmatize the content of HTML pages (branch `feature/preprocessing`)
  
##### Boolean search
  Create inverted index and use boolean search (branch `feature/inverted-index__boolean-search`)
  Query example:
  ```
    fortune OR fortify AND NOT forteana
  ```

## Running the project
1. Install `python 3` and `virtualenv` (if not)
2. Clone the repo
3. Create a virtualenv
    ```
    cd info-search-project
    virtualenv -p python3 ./venv
    ```
4. Activate virtualenv

    **Windows**
    ```
    .\venv\Scripts\activate
    ```
    **MacOS/Linux**
    ```
    source ./venv/bin/activate
    ```
5. Install requirements from `requirements.txt` file
    ```
    pip install -r requirements.txt
    ```
    
6. To use Crawler run the script:
    ```
    python main.py <MAX_PAGES_NUM> <WIKI_SECTION>
    ```
    Default: `python main.py 100 Astronomy`

## Techologies
 - Python
 - BeautifulSoup4
