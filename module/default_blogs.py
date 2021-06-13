from module.web_scraper import WebScraper, Item

def scrape_travelsmart():
    travel_smart = WebScraper("https://www.travelsmart.bg/")
    travel_smart.add_items( Item('content', 'div', {'class': 'post-content'}) )
    travel_smart.scrape_to_csv(20, "output/travelsmart.csv")
    
def scrape_bozho():
    bozho = WebScraper("https://blog.bozho.net/")
    bozho.add_items( Item('content', 'div', {'class' : 'post-content'}) )
    bozho.scrape_to_csv(20, 'output/bozho')
    
def scrape_pateshestvenik():
    pateshestvenik = WebScraper("https://pateshestvenik.com/")
    pateshestvenik.add_items(Item('content', 'div', {'class' : 'content'}) )
    pateshestvenik.scrape_to_csv(20, 'output/pateshestvenik')
    
def scrape_az_moga():
    az_moga = WebScraper("https://az-moga.com/")
    az_moga.add_items( Item('content', 'div', {'class' : 'entry-body'}) )
    az_moga.scrape_to_csv(20, 'output/az_moga')
    
def scrape_igicheva():
    igicheva = WebScraper("https://igicheva.wordpress.com/all-posts/")
    igicheva.add_items( Item('headline', 'h1', {'class': 'entry-title'}) )
    igicheva.set_article_search_item(Item('', 'article', {'class': 'type-post'}))
    igicheva.scrape_to_csv(20, 'output/igicheva')

predefined_blogs = { 
    'travelsmart': scrape_travelsmart,
    'bozho' : scrape_bozho,
    'pateshestvenik' : scrape_pateshestvenik,
    'az_moga' : scrape_az_moga,
    'igicheva' : scrape_igicheva
}