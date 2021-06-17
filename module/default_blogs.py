from module.web_scraper import WebScraper, Item


def travelsmart():
    travel_smart = WebScraper("https://www.travelsmart.bg/")
    travel_smart.add_items( Item('content', 'div', {'class': 'post-content'}),
                            Item('comment-author', 'div', {'class': 'comment-author'}),
                            Item('comment-text', 'div', {'class': 'comment-text'}) 
                           )
    return travel_smart


def bozho():
    bozho = WebScraper("https://blog.bozho.net/")
    bozho.add_items( Item('content', 'div', {'class' : 'post-content'}), 
                     Item('comment-author', 'div', {'class' : 'comment-author'}),
                     Item('comment-text', 'div', {'class': 'comment-content'}) 
                    )
    return bozho

#comments
def pateshestvenik():
    pateshestvenik = WebScraper("https://pateshestvenik.com/")
    pateshestvenik.add_items( Item('content', 'div', {'class' : 'content'}), 
                              Item('comment-author', 'a', {'class' : 'UFICommentActorName'}),
                              Item('comment-text', 'span', {'class': '_5mdd'})
                            )
    return pateshestvenik


def az_moga():
    az_moga = WebScraper("https://az-moga.com/")
    az_moga.add_items( Item('content', 'div', {'class' : 'entry-body'}), 
                       Item('comment-author', 'div', {'class' : 'comment-author'}),
                       Item('comment-text', 'div', {'class': 'comment-content'})
                     )
    return az_moga


def igicheva():
    igicheva = WebScraper("https://igicheva.wordpress.com/all-posts/")
    igicheva.add_items( Item('headline', 'h1', {'class': 'entry-title'}), 
                        Item('comment-author', 'div', {'class' : 'comment-author'}),
                        Item('comment-text', 'div', {'class': 'comment-content'})
                       )
    igicheva.set_article_search_item(Item('', 'article', {'class': 'type-post'}))
    return igicheva


predefined_blogs = { 
    'travelsmart': travelsmart,
    'bozho' : bozho,
    'pateshestvenik' : pateshestvenik,
    'az_moga' : az_moga,
    'igicheva' : igicheva
}
