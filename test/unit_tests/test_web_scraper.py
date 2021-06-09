from bs4 import BeautifulSoup
from module.web_scraper import WebScraper, Item

from unittest.mock import patch
import pytest


@staticmethod
def soupify_mock(url):
    file = open("test/html/" + url, "r")
    return BeautifulSoup(file, 'lxml')

def test_init():
    scraper = WebScraper(   "https://example.net",
                            Item('content', 'div', {'class': 'post-content'}),
                            Item('site', 'meta', {'property': 'og:site_name'}) )

    expected_names = [ 'headline', 'date', 'content', 'site' ]
    expected_tags =  [ 'h1', 'meta', 'div', 'meta' ]
    expected_attributes = [ {'':''}, {'property': 'article:published_time'}, 
                            {'class': 'post-content'}, {'property': 'og:site_name'} ]

    for i in range(len(expected_names)):
        assert scraper.items[i].name == expected_names[i]
        assert scraper.items[i].tag == expected_tags[i]
        assert scraper.items[i].attribute == expected_attributes[i]


def test_generate_page_url(default_scraper: WebScraper):
    generator = default_scraper.generate_page_url()

    assert generator.__next__() == "https://example.net"

    for page in range(2, 12):
        assert generator.__next__() == f"https://example.net/page/{page}"


@patch("module.web_scraper.WebScraper.soupify_webpage", soupify_mock)
def test_generate_webpage_soup(default_scraper: WebScraper, example_page_soups):

    with pytest.raises(Exception):
        for i, soup in enumerate(default_scraper.generate_webpage_soup()):
            assert soup == example_page_soups[i]


@patch("module.web_scraper.WebScraper.soupify_webpage", soupify_mock)
def test_get_article_soup(default_scraper: WebScraper,
                          example_page_soups, example_post_soups):

    for page in example_page_soups:
        for soup in default_scraper.get_article_soup(page):
            assert soup == example_post_soups[0]


def test_scrape_article_item(default_scraper: WebScraper, custom_scraper : WebScraper, 
                             example_post_soups, example_post_content):

    for i, item in enumerate(default_scraper.items):
        scraped = default_scraper.scrape_article_item(example_post_soups[0], item)
        assert scraped == example_post_content[i]

    for i, item in enumerate(custom_scraper.items):
        scraped = custom_scraper.scrape_article_item(example_post_soups[1], item)
        if item.name == 'date':
            assert scraped == None
        else:
            assert scraped == example_post_content[i]


def test_scrape_article(example_post_soups, example_post_content):
    assert WebScraper("").scrape_article(
        example_post_soups[0]) == example_post_content
    #TODO: scrape more than 3 items