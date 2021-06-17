from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from module.web_scraper import WebScraper, Item

import pandas as pd
from unittest.mock import patch
import pytest


@staticmethod
def soupify_mock(url):
    try:
        file = open("test/html/" + url, "r")
    except:
        raise RequestException
    return BeautifulSoup(file, 'lxml')


def page_url_mock(_):
    yield "Example.html"
    yield "page/2"
    yield "page/3"
    yield "page/4"


def test_add_items(expected_init):
    scraper = WebScraper("https://example.net")
    scraper.add_items( Item('content', 'div', {'class': 'post-content'}),
                       Item('site', 'meta', {'property': 'og:site_name'}) )

    i = 0
    for item in scraper.items:
        assert item.name == expected_init['names'][i]
        assert item.tag == expected_init['tags'][i]
        assert item.attribute == expected_init['attributes'][i]
        i += 1
    
    assert i == len(expected_init['names'])


def test_generate_page_url(default_scraper: WebScraper):
    generator = default_scraper.generate_page_url()

    assert generator.__next__() == "https://example.net"

    for page in range(2, 20): # don't expect /page/1
        assert generator.__next__() == f"https://example.net/page/{page}"


@patch("module.web_scraper.WebScraper.soupify_webpage", soupify_mock)
@patch("module.web_scraper.WebScraper.generate_page_url", page_url_mock)
def test_generate_webpage_soup(default_scraper: WebScraper, example_page_soups):

    with pytest.raises(RequestException):
        for i, soup in enumerate(default_scraper.generate_webpage_soup()):
            assert soup == example_page_soups[i]
        

@patch("module.web_scraper.WebScraper.soupify_webpage", soupify_mock)
def test_generate_article_soup(default_scraper: WebScraper,
                               example_page_soups, example_post_soups):

    for page in example_page_soups:
        for soup in default_scraper.generate_article_soup(page):
            assert soup == example_post_soups[0]


def test_scrape_article_item(default_scraper: WebScraper, custom_scraper : WebScraper, 
                             example_post_soups, example_post_content):

    for i, item in enumerate(default_scraper.items):
        scraped = default_scraper.scrape_article_items(example_post_soups[0], item)
        assert scraped == example_post_content[i]

    for i, item in enumerate(custom_scraper.items):
        scraped = custom_scraper.scrape_article_items(example_post_soups[1], item)
        if item.name == 'date':
            assert scraped is None
        else:
            assert scraped == example_post_content[i]


def test_scrape_article(default_scraper, example_post_soups, example_post_content):
    assert default_scraper.scrape_article(
        example_post_soups[0]) == example_post_content
    
    scraper = WebScraper("https://example.net")
    scraper.add_items( Item('content', 'div', {'class': 'post-content'}),
                       Item('site', 'meta', {'property': 'og:site_name'}) )
    
    example_post_content.append('Example')
    example_post_content[1] = None

    assert scraper.scrape_article(
        example_post_soups[1]) == example_post_content


def test_init_data_frame(default_scraper):
    default_scraper.init_data_frame()

    assert isinstance(default_scraper.df, pd.DataFrame)


@patch("module.web_scraper.WebScraper.soupify_webpage", soupify_mock)
@patch("module.web_scraper.WebScraper.generate_page_url", page_url_mock)
def test_scrape(default_scraper, example_df):
    max_posts = 5

    assert default_scraper.scrape(3) == 3
    assert default_scraper.scrape(20) == max_posts
    assert default_scraper.df.equals(example_df)
