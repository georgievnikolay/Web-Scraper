import requests
from requests import RequestException
from bs4 import BeautifulSoup

import pandas as pd


class Item:
    """
    An Item object represents the signature of an HTML tag.
    """

    def __init__(self, name: str, tag: str, attribute=None):  # pragma: no cover
        """
        Constructor.
        
        :name: used for internal categorization, eg when writing to a file.
        To replace a default Item, it must coincide with the default name. \n
        :tag: the HTML tag of the element, eg 'a', 'div', etc. \n
        :attribute: an (optional) dictionary consisting of identifying properties,
        eg 'class':'content', 'id':'title', etc.
        """
        self.name = name
        self.tag = tag
        if attribute is None:
            self.attribute = {'': ''}
        else:
            self.attribute = attribute
    
    def set(self, item): # pragma: no cover
        self.name = item.name
        self.tag = item.tag
        self.attribute = item.attribute


class WebScraper:
    """
    This webscraper has been designed mainly to work on WordPress-based blogs.
    
    For some websites, it will be enough to initialize it with the main URL,
    then call the scrape_to_csv() function.
    This should scrape each article's headline, publish date, and text content.
    
    If these items are not configured per WP's defaults, it is necessary
    to provide their specific signature: the element type (tag), eg 'div', 'h2', etc;
    and any uniquely identifying property, eg 'class content', 'id headline', etc.
    This is done using Item objects.
    Use set_article_search_item() if the link to each article is not found correctly:
    pass an appropriate Item with uniquely identifying attributes.
    """

    def __init__(self, url): # pragma: no cover
        """
        Constructor.
        Initializes Item objects corresponding to WordPress's defaults.
        """
        self.url = url
        self.items = [  Item('headline', 'h1'),
                        Item('date', 'meta', {'property': 'article:published_time'}),
                        Item('content', 'div', {'class': 'entry-content'}) ]
        
        self.article_item = Item('', 'article', {'':''})
        self.df = None    

    def add_items(self, *items : Item):
        """
        Adds new Items to scrape. If an Item's name coincides with
        'headline', 'date' or 'content', it will replace the default.
        """
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
        Requests the page at url and returns a corresponding BeautifulSoup object.
        If the request fails, a RequestException is raised.
        """
        success_status = 200

        response = requests.get(url)
        if response.status_code != success_status:
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

    def set_article_search_item(self, item): # pragma: no cover
        """
        Sets the signature by which to find article links.
        The default is any 'article' element.
        """
        self.article_item.set(item)

    def generate_article_soup(self, page_soup):
        """
        Generator that yields the soup of every article 
        found on the given high-level page.
        """

        for article in page_soup.find_all(self.article_item.tag, self.article_item.attribute):
            article_link = article.find('a')['href']
            yield self.soupify_webpage(article_link)

    @staticmethod
    def scrape_article_items(article_soup, item: Item):
        """ 
        Attempts to find elements with the item's signature
        within the BeautifulSoup of an article.
        Returns a string if one element is found,
        and a list of strings if there are multiple.
        """
        found_items = article_soup.find_all(item.tag, item.attribute)
        
        if not found_items:
            return None

        try:
            contents = [item['content'] for item in found_items]
        except KeyError: # An item was found, but it has no 'content' attribute
            contents = [item.text for item in found_items]

        return contents if len(contents) > 1 else contents[0]

    def scrape_article(self, article_soup):
        """
        Scrapes the given article for the specified items.
        Returns them in a list of strings.
        """

        scraped_items = []
        for item in self.items:
            new = self.scrape_article_items(article_soup, item)
            scraped_items.append(new)

        return scraped_items

    def init_data_frame(self):
        """
        Creates a DataFrame object with columns corresponding
        the names of the Item objects of the instance.
        """
        field_names = [item.name for item in self.items]
        self.df = pd.DataFrame(columns=field_names)

    def scrape(self, num_of_articles):
        """
        Scrapes the given number of latest articles 
        and writes them to a data frame in named columns.
        """
        num_scraped = 0

        self.init_data_frame()

        try:
            for page_soup in self.generate_webpage_soup(): # pragma: no branch
                for article_soup in self.generate_article_soup(page_soup):
                    scraped_items = self.scrape_article(article_soup)
                    
                    self.df.loc[num_scraped] = scraped_items

                    num_scraped += 1
                    if num_scraped == num_of_articles:
                        return num_scraped

        except RequestException:
            print(f"Only {num_scraped} articles found.")
            return num_scraped

    def export_to_csv(self, filename): # pragma: no cover
        self.df.to_csv(filename, index=False, encoding='utf-8-sig')

    def export_to_json(self, filename): # pragma: no cover
        self.df.to_json(filename, force_ascii=False, orient='records', indent=4)
