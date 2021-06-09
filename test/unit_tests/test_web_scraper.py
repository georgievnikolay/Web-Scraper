from bs4 import BeautifulSoup
from module.web_scraper import WebScraper, Item

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
def test_generate_webpage_soup(example_pages):

    with pytest.raises(Exception):
        for i, soup in enumerate(WebScraper("").generate_webpage_soup()):
            assert soup == example_pages[i]
            if i == 2:
                break


@patch("module.web_scraper.WebScraper.soupify_webpage", soupify_mock)
def test_get_article_soup(example_pages, example_posts):

    for page in example_pages:
        scraper_gen = WebScraper("").get_article_soup(page)
        assert scraper_gen.__next__() == example_posts[0]


def test_scrape_article_item(example_posts, example_post_content):
    scraper = WebScraper("")
    for item in scraper.items:
        print(item.name, item.tag, item.attribute)

    for index in range(len(scraper.items)):
        assert scraper.scrape_article_item(example_posts[0], scraper.items[index]) \
            == example_post_content[index]


def test_scrape_article(example_posts, example_post_content):
    assert WebScraper("").scrape_article(
        example_posts[0]) == example_post_content
