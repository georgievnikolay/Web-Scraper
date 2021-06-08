import requests
from bs4 import BeautifulSoup

class WebScraper:
    """
    WebScraper:
    """

    def __init__(self, url,
                 headline_tag='h1',
                 headline_attr=('', ''),
                 date_tag='meta',
                 date_attr=('property', 'article:published_time'),
                 content_tag='div',
                 content_attr=('class', 'entry-content')
                 ):

        self.url = url
        self.headline = ( headline_tag, { headline_attr[0] : headline_attr[1]} )
        self.date =     ( date_tag,     { date_attr[0] : date_attr[1]} )
        self.content =  ( content_tag,  { content_attr[0] : content_attr[1]} )
        
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
    def soupify_webpage(url): # pragma: no cover
        """
        """
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception #TODO: more specific exception
        return BeautifulSoup(response.text, 'lxml')

    def generate_webpage_soup(self):
        """
        Generator that yields the soup of each high-level page.
        """

        for url in self.generate_page_url():
            try:
                yield self.soupify_webpage(url)
            except Exception as ex: #TODO: same as before
                print(f"Page {url} not found.")
                raise ex

    def get_article_soup(self, page_soup):
        """
        Generator that yields the soup of every article 
        found on the given high-level page.
        """

        for article in page_soup.find_all('article'):
            article_link = article.find('a')['href']
            yield self.soupify_webpage(article_link)

    def scrape_article_item(self, article_soup, item):
        try:
            return article_soup.find(*item)['content']
        except:
            return article_soup.find(*item).text

    def scrape_article(self, article_soup):
        """
        Scrapes the given article for its headline, date, and content.
        Returns them in a list.
        """
        items_to_scrape = [self.headline, self.date, self.content]
        # return [self.scrape_article_item(article_soup, item) for item in items_to_scrape]
        
        scraped_items = []
        for item in items_to_scrape:
            new = self.scrape_article_item(article_soup, item)
            scraped_items.append(new)

        return scraped_items

    def scrape_to_csv(self, num_of_articles):
        """
        Scrapes the given number of latest articles 
        and writes them to a csv file in three columns.
        """
        pass
