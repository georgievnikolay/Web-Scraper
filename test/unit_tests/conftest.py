"""
Configuration for pytest.

NOTE: This file is automatically included when running pytest.
      There is no need to import it explicitly in the test files.
"""

import os
import sys
import pytest
from bs4 import BeautifulSoup

# allow the contents to be found automatically as if we were in that directory
sys.path.append(
    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
)

@pytest.fixture
def example_html():
    with open("./test/html/Example.html", "r") as html_file:
        soup = BeautifulSoup(html_file, 'lxml')
    return soup

@pytest.fixture
def example_page2():
    with open("./test/html/page/2", "r") as html_file:
        soup = BeautifulSoup(html_file, 'lxml')
    return soup

@pytest.fixture
def example_page3():
    with open("./test/html/page/3", "r") as html_file:
        soup = BeautifulSoup(html_file, 'lxml')
    return soup

@pytest.fixture
def example_post():
    with open("./test/html/ExamplePost.html", "r") as html_file:
        soup = BeautifulSoup(html_file, 'lxml')
    return soup

@pytest.fixture
def example_post_content():
    headline = "Example Post"
    date = "2014-04-30T10:15:33+00:00"
    content =   "\nThis domain is for use in illustrative examples in documents. You may use this" \
                    "\ndomain in literature without prior coordination or asking for permission." \
                    "\nHome page...\n"
    
    return [headline, date, content]