import requests
from requests import RequestException
from bs4 import BeautifulSoup


class Item:

    def __init__(self, name: str, tag: str, attribute={'': ''}):  # pragma: no cover
        self.name = name
        self.tag = tag
        self.attribute = attribute

    def set(self, item): # pragma: no cover
        self.name = item.name
        self.tag = item.tag
        self.attribute = item.attribute


class WebScraper(Item):
    """
    WebScraper:
    """

    def __init__(self, url, *items: Item):
        self.url = url
        self.items = [  Item('headline', 'h1'),
                        Item('date', 'meta', {'property': 'article:published_time'}),
                        Item('content', 'div', {'class': 'entry-content'}) ]

        for new_item in items:
            found = False
            
            for default_item in self.items:
                if new_item.name == default_item.name:
                    default_item.set(new_item)
                    found = True
            
            if not found:
                self.items.append(new_item)


    def generate_page_url(self):
        """
        Generator that yields high-level page urls:
        starts at the base url provided at initialization,
        then appends /page/[n], incrementing n with each call.
        """
        yield self.url
        page_num = 1

        while True:
            page_num += 1
            full_url = self.url + f"/page/{page_num}"
            yield full_url

    @staticmethod
    def soupify_webpage(url):  # pragma: no cover
        """
        """
        response = requests.get(url)
        if response.status_code != 200:
            raise RequestException

        return BeautifulSoup(response.text, 'lxml')

    def generate_webpage_soup(self):
        """
        Generator that yields the soup of each high-level page.
        """

        for url in self.generate_page_url(): # pragma: no branch
            try:
                yield self.soupify_webpage(url)

            except RequestException as ex:
                print(f"Request to get {url} failed.")
                raise ex


    def get_article_soup(self, page_soup):
        """
        Generator that yields the soup of every article 
        found on the given high-level page.
        """

        for article in page_soup.find_all('article'):
            article_link = article.find('a')['href']
            yield self.soupify_webpage(article_link)

    def scrape_article_item(self, article_soup, item: Item):
        try:
            return article_soup.find(item.tag, item.attribute)['content']
        except:
            try:
                return article_soup.find(item.tag, item.attribute).text
            except:
                return None

    def scrape_article(self, article_soup):
        """
        Scrapes the given article for the specified items.
        Returns them in a list.
        """

        scraped_items = []
        for item in self.items:
            new = self.scrape_article_item(article_soup, item)
            scraped_items.append(new)

        return scraped_items

    def scrape_to_csv(self, num_of_articles):
        """
        Scrapes the given number of latest articles 
        and writes them to a csv file in named columns.
        """
        pass
