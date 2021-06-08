import pytest
from module.web_scraper import WebScraper

@pytest.fixture
def local_scraper():
    return WebScraper("/test/html/Example.html")

def test_generate_page_url(local_scraper):
    generator = local_scraper.generate_page_url()
    
    assert generator.__next__() == "/test/html/Example.html"
    
    for page in range(2, 12):
        assert generator.__next__() == f"/test/html/Example.html/page/{page}"

