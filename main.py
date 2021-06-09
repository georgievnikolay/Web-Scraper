#!/usr/bin/env python3

from module.web_scraper import WebScraper, Item # pragma: no cover

if __name__ == "__main__": 
    travel_smart = WebScraper(  "https://www.travelsmart.bg/", 
                                Item('content', 'div', {'class': 'post-content'}) )

    travel_smart.scrape_to_csv(20, "travelsmart.csv")

    # Examples to try with other blogs and more items

    # travel_smart = WebScraper("https://www.travelsmart.bg/", 
    #                           Item('content', 'div', {'class': 'post-content'}),
    #                           Item('modified', 'meta', {'property': 'article:modified_time'}))
    # travel_smart.scrape_to_csv(20, "travelsmart.csv")

    # bozho = WebScraper( "https://blog.bozho.net/", 
    #                     Item('content', 'div', {'class' : 'post-content'}) )
    # bozho.scrape_to_csv(20, 'bozho')

    # igicheva = WebScraper("https://igicheva.wordpress.com/all-posts/")
    # igicheva.scrape_to_csv(20, 'igicheva')

    # pateshestvenik = WebScraper("https://pateshestvenik.com/", 
    #                             Item('content', 'div', {'class' : 'content'}) )
    # pateshestvenik.scrape_to_csv(20, 'pateshestvenik')

    # az_moga = WebScraper("https://az-moga.com/", 
    #                       Item('content', 'div', {'class' : 'content'}) )
    # az_moga.scrape_to_csv(20, 'az_moga')
