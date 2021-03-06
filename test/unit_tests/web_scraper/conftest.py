"""
Configuration for pytest.

NOTE: This file is automatically included when running pytest.
      There is no need to import it explicitly in the test files.
"""

import os
import sys

import pytest

from module.web_scraper import WebScraper, Item
from bs4 import BeautifulSoup
import pandas as pd

# allow the contents to be found automatically as if we were in that directory
sys.path.append(
    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
)


@pytest.fixture
def expected_init():
    names = [ 'headline', 'date', 'content', 'site' ]
    tags =  [ 'h1', 'meta', 'div', 'meta' ]
    attributes = [ {'':''}, {'property': 'article:published_time'}, 
                            {'class': 'post-content'}, {'property': 'og:site_name'} ]
    
    return {'names': names, 'tags': tags, 'attributes': attributes} 


@pytest.fixture
def default_scraper():
    return WebScraper("https://example.net")


@pytest.fixture
def custom_scraper():
    scraper = WebScraper("https://example.net")
    scraper.add_items( Item('content', 'div', {'class': 'post-content'}) )
    return scraper


@pytest.fixture
def example_page_soups():
    files = [ open("./test/html/Example.html", 'r', encoding='utf-8-sig'),
              open("./test/html/page/2", 'r', encoding='utf-8-sig'),
              open("./test/html/page/3", 'r', encoding='utf-8-sig') ]
    soups = []
    for f in files:
        soups.append(BeautifulSoup(f, 'html.parser'))
        f.close()

    return soups


@pytest.fixture
def example_post_soups():
    files = [open("./test/html/ExamplePost.html", 'r', encoding='utf-8-sig'),
             open("./test/html/ExamplePost2.html", 'r', encoding='utf-8-sig')]
    soups = []
    for f in files:
        soups.append(BeautifulSoup(f, 'html.parser'))
        f.close()

    return soups


@pytest.fixture
def example_post_content():
    headline =  "Example Post"
    date =      "2014-04-30T10:15:33+00:00"
    content =   "\nThis domain is for use in illustrative examples in documents. You may use this" \
                "\ndomain in literature without prior coordination or asking for permission." \
                "\nHome page...\n"

    return [headline, date, content]


@pytest.fixture
def example_df():
    df = pd.read_csv('./test/unit_tests/web_scraper/example.csv')
    return df
