import requests
from requests import RequestException
from bs4 import BeautifulSoup
import csv

class Item:
    """
    An Item object represents the signature of an HTML tag.
    """

    def __init__(self, name: str, tag: str, attribute={'': ''}):  # pragma: no cover
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
        self.attribute = attribute

    def set(self, item): # pragma: no cover
        self.name = item.name
        self.tag = item.tag
        self.attribute = item.attribute


class WebScraper(Item):
    """
    This webscraper has been designed mainly to work on WordPress-based blogs.
    
    For some websites, it will be enough to initialize it with the main URL,
    then call the scrape_to_csv() function.
    This should scrape each article's headline, publish date, and text content.
    
    If these items are not configured per WP's defaults, it is necessary
    to provide their specific signature: the element type (tag), eg 'div', 'h2', etc;
    and any uniquely identifying property, eg 'class content', 'id headline', etc.
    This is done using Item objects.
    """

    def __init__(self, url, *items: Item):
        """
        Constructor. Provide Item objects where the WP defaults do not suffice.
        
        If an Item's name coincides with 'headline', 'date', or 'content',
        it will replace the default. Otherwise, it will be added to the list
        of items to scrape.
        """
        self.url = url
        self.items = [  Item('headline', 'h1'),
                        Item('date', 'meta', {'property': 'article:published_time'}),
                        Item('content', 'div', {'class': 'entry-content'}) ]
        self.csv_file = None

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
        Request the page at url and return a corresponding BeautifulSoup object.
        If the request fails, a RequestException is raised.
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


    def generate_article_soup(self, page_soup):
        """
        Generator that yields the soup of every article 
        found on the given high-level page.
        """

        for article in page_soup.find_all('article'):
            article_link = article.find('a')['href']
            yield self.soupify_webpage(article_link)

    def scrape_article_item(self, article_soup, item: Item):
        """
        Attempt to find an element corresponding to the given item's signature
        within the given BeautifulSoup object. Return a string of its text contents.
        """
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
        Returns them in a list of strings.
        """

        scraped_items = []
        for item in self.items:
            new = self.scrape_article_item(article_soup, item)
            scraped_items.append(new)

        return scraped_items

    def init_csv_file(self, filename):
        """
        Open the specified file for writing. Write the item names as column names.
        Return the CSV writer object to be used for the scraped data.
        """
        field_names = [item.name for item in self.items]

        if not ".csv" in filename:
            filename += ".csv"
        
        self.csv_file = open(filename, 'w', newline='', encoding='utf-8')
        
        writer = csv.writer(self.csv_file)
        writer.writerow(field_names)

        return writer

    def scrape_to_csv(self, num_of_articles, filename): # pragma: no cover
        """
        Scrapes the given number of latest articles 
        and writes them to a csv file in named columns.
        """
        num_scraped = 0

        writer = self.init_csv_file(filename)

        try:
            for page_soup in self.generate_webpage_soup():
                for article_soup in self.generate_article_soup(page_soup):
                    scraped_items = self.scrape_article(article_soup)
                    writer.writerow(scraped_items)

                    num_scraped += 1
                    if num_scraped == num_of_articles:
                        self.csv_file.close()
                        return num_scraped

        except RequestException:
            print(f"Only {num_scraped} articles found.")
            self.csv_file.close()
            return num_scraped

