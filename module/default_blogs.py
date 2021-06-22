from module.data_formatter import DataFormatter
from module.web_scraper import WebScraper, Item


class Blog:
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
