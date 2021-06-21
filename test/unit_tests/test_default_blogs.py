from module.default_blogs import Blog
from module.web_scraper import WebScraper
from module.data_formatter import DataFormatter


def test_not_supported():
    assert Blog.not_supported('truly-unsupported') == True
    assert Blog.not_supported('bozho') == False

def test_scraper():
    Blog.scraper("travelsmart") # branch
    scraper = Blog.scraper("igicheva")
    assert isinstance(scraper, WebScraper)
    assert scraper.url == "https://igicheva.wordpress.com/all-posts/"

def test_formatter():
    Blog.formatter("travelsmart") # branch
    formatter = Blog.formatter("igicheva")
    assert isinstance(formatter, DataFormatter)
