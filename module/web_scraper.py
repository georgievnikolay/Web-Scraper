class Scraper:

    def __init__(self, url, 
                 headline=[ 'h1', {} ], 
                 content=[ 'div', { 'class': 'fusion-text' } ], 
                 date=[ 'span', { 'class': 'rich-snippet-hidden' } ]):

        self.url = url
        self.headline = headline
        self.content = content
        self.date = date


    def load_page(self):
        pass

    def scrape_headline(self):
        pass

    def scrape_content(self):
        pass

    def scrape_date(self):
        pass

    def scrape_articles(self, n):
        pass


if __name__ == '__main__':
    ex1 = Scraper('example.org')

    ex2 = Scraper('example.com', headline=['h2', {}])

    ex3 = Scraper(  'all-custom.com', 
                    headline=['h1', {'class': 'headline'}],
                    content=['article', {}],
                    date=['a', {'some-property': 'some-value'}])

    ex3.scrape_articles(20)