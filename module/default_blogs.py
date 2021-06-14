from module.web_scraper import WebScraper, Item

def travelsmart():
    travel_smart = WebScraper("https://www.travelsmart.bg/")
    travel_smart.add_items( Item('content', 'div', {'class': 'post-content'}) )
    return travel_smart

def bozho():
    bozho = WebScraper("https://blog.bozho.net/")
    bozho.add_items( Item('content', 'div', {'class' : 'post-content'}) )
    return bozho
    
def pateshestvenik():
    pateshestvenik = WebScraper("https://pateshestvenik.com/")
    pateshestvenik.add_items(Item('content', 'div', {'class' : 'content'}) )
    return pateshestvenik
    
def az_moga():
    az_moga = WebScraper("https://az-moga.com/")
    az_moga.add_items( Item('content', 'div', {'class' : 'entry-body'}) )
    return az_moga
    
def igicheva():
    igicheva = WebScraper("https://igicheva.wordpress.com/all-posts/")
    igicheva.add_items( Item('headline', 'h1', {'class': 'entry-title'}) )
    igicheva.set_article_search_item(Item('', 'article', {'class': 'type-post'}))
    return igicheva

predefined_blogs = { 
    'travelsmart': travelsmart,
    'bozho' : bozho,
    'pateshestvenik' : pateshestvenik,
    'az_moga' : az_moga,
    'igicheva' : igicheva
}