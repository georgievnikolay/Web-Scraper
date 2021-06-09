#!/usr/bin/env python3

from module.web_scraper import WebScraper, Item # pragma: no cover

if __name__ == "__main__": 
    travel_smart = WebScraper("https://www.travelsmart.bg/", 
                              Item('content', 'div', {'class': 'post-content'}) )

    travel_smart.scrape_to_csv(20, "travelsmart.csv")


    # # # Working examples with the other blogs # # #
    # Just uncomment and run

    # travel_smart = WebScraper("https://www.travelsmart.bg/", 
    #                           Item('content', 'div', {'class': 'post-content'}),
    #                           Item('modified', 'meta', {'property': 'article:modified_time'}))
    # travel_smart.scrape_to_csv(20, "travelsmart_mod.csv")


    # bozho = WebScraper("https://blog.bozho.net/", 
    #                    Item('content', 'div', {'class' : 'post-content'}) )
    # bozho.scrape_to_csv(20, 'bozho')


    # pateshestvenik = WebScraper("https://pateshestvenik.com/", 
    #                             Item('content', 'div', {'class' : 'content'}) )
    # pateshestvenik.scrape_to_csv(20, 'pateshestvenik')


    # az_moga = WebScraper("https://az-moga.com/", 
    #                       Item('content', 'div', {'class' : 'entry-body'}) )
    # az_moga.scrape_to_csv(20, 'az_moga')


    # igicheva = WebScraper("https://igicheva.wordpress.com/all-posts/",
    #                       Item('headline', 'h1', {'class': 'entry-title'}) )
    # igicheva.scrape_to_csv(20, 'igicheva')
