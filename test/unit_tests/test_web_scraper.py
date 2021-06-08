from bs4 import BeautifulSoup
from module.web_scraper import WebScraper

from unittest.mock import patch
import pytest

# @pytest.fixture
# def local_scraper():
#     return WebScraper("/test/html/Example.html")

@staticmethod
def soupify_mock(url):
    file = open("test/html/" + url, "r")
    return BeautifulSoup(file, 'lxml')

def test_generate_page_url():
    generator = WebScraper("https://example.net").generate_page_url()
    
    assert generator.__next__() == "https://example.net"
    
    for page in range(2, 12):
        assert generator.__next__() == f"https://example.net/page/{page}"

@patch("module.web_scraper.WebScraper.soupify_webpage", soupify_mock)
def test_generate_webpage_soup(example_html, example_page2, example_page3):
    expected = [example_html, example_page2, example_page3]

    with pytest.raises(Exception):
        for i, soup in enumerate(WebScraper("").generate_webpage_soup()):
            assert soup == expected[i]
            if i == 2: break

@patch("module.web_scraper.WebScraper.soupify_webpage", soupify_mock)
def test_get_article_soup(example_html, example_post):
    for result in WebScraper("").get_article_soup(example_html):
        assert result == example_post

def test_scrape_article_item(example_post, example_post_content):   
    scraper = WebScraper("")

    article_items = [scraper.headline, scraper.date, scraper.content]

    for index in range(2):
        assert scraper.scrape_article_item(example_post, article_items[index]) == example_post_content[index]
        
def test_scrape_article(example_post, example_post_content):
    assert WebScraper("").scrape_article(example_post) == example_post_content
