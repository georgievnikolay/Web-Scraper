from module.data_formatter import DataFormatter
from module.web_scraper import WebScraper, Item
from module.data_handler import DataHandler

from os import path

class Blog:
    path = path.join(path.dirname(path.dirname(__file__)), f'output/')

    urls = {
        'travelsmart': "https://www.travelsmart.bg/",
        'bozho' : "https://blog.bozho.net/",
        'pateshestvenik' : "https://pateshestvenik.com/",
        'az_moga' : "https://az-moga.com/",
        'igicheva' : "https://igicheva.wordpress.com/all-posts/"
    }

    scraper_items = {
        'travelsmart':    [ Item('content', 'div', {'class': 'post-content'}),
                            Item('comment-author', 'div', {'class': 'comment-author'}),
                            Item('comment-text', 'div', {'class': 'comment-text'}) ],
                            
        'bozho':          [ Item('content', 'div', {'class' : 'post-content'}), 
                            Item('comment-author', 'div', {'class' : 'comment-author'}),
                            Item('comment-text', 'div', {'class': 'comment-content'}) ],
                            
        'pateshestvenik': [ Item('content', 'div', {'class' : 'content'}), 
                            Item('comment-author', 'a', {'class' : 'UFICommentActorName'}),
                            Item('comment-text', 'span', {'class': '_5mdd'}) ],

        'az_moga':        [ Item('content', 'div', {'class' : 'entry-body'}), 
                            Item('comment-author', 'div', {'class' : 'comment-author'}),
                            Item('comment-text', 'div', {'class': 'comment-content'}) ],

        'igicheva':       [ Item('headline', 'h1', {'class': 'entry-title'}), 
                            Item('comment-author', 'div', {'class' : 'comment-author'}),
                            Item('comment-text', 'div', {'class': 'comment-content'}) ]
    }

    search_items = {
        'igicheva': Item('', 'article', {'class': 'type-post'})
    }

    author_extract = { # pragma: no branch
        'bozho': lambda s: s.split(' каза:')[0][2:],
        'az_moga': lambda s: s.split(' каза:')[0][2:],
        'igicheva': lambda s: s.split(' says:')[0][2:]
    }

    @classmethod
    def not_supported(cls, website):
        if website in cls.urls.keys():
            return False
        else:
            return True
            
    @classmethod
    def scraper(cls, website):
        scraper = WebScraper(cls.urls[website])
        scraper.add_items(*cls.scraper_items[website])
        if website in cls.search_items:
            scraper.set_article_search_item(cls.search_items[website])

        return scraper

    @classmethod
    def formatter(cls, website):
        formatter = DataFormatter()

        if website in cls.author_extract:
            formatter.set_author_extract_func(cls.author_extract[website])

        return formatter

    @classmethod # pragma: no cover
    def scrape_to_file(cls, website, number):
        try:
            scraper = cls.scraper(website)
            scraper.scrape(number)
            DataHandler.data_frame_to_json(scraper.df, path.join(cls.path, f'{website}.json'))
        except PermissionError:
            print(f"Access denied. Failed to write {website}.json.")
            exit(3)
    
    @classmethod # pragma: no cover
    def format_from_file(cls, website):
        try:
            formatter = Blog.formatter(website)
            preformat_data = DataHandler.json_to_obj(path.join(cls.path, f'{website}.json'))
            result = formatter.format(preformat_data)
            DataHandler.obj_to_json(result, path.join(cls.path, f'{website}_formatted.json'))
        except FileNotFoundError:
            print(f"No data to format. {website}.json not found in output/ dir.")
            exit(2)
        except PermissionError:
            print(f"Access denied. Failed to write {website}_formatted.json.")
            exit(3)
            
    @classmethod # pragma: no cover
    def scrape_and_format(cls, website, number):
        scraper = cls.scraper(website)
        scraper.scrape(number)
        preformat_data = scraper.df.to_dict(orient='records')
        
        try:
            formatter = Blog.formatter(website)
            result = formatter.format(preformat_data)
            DataHandler.obj_to_json(result, path.join(cls.path, f'{website}_formatted.json'))
        except PermissionError:
            print(f"Access denied. Failed to write {website}_formatted.json.")
            exit(3)
