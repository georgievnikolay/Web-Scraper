#!/usr/bin/env python3

from module.web_scraper import WebScraper, Item # pragma: no cover
from module.data_formatter import DataFormatter
from module.default_blogs import predefined_blogs
import argparse
import os

def parse_args():  # pragma: no cover
    """Parse the input args."""
    parser = argparse.ArgumentParser(
        description="WebScraper"
    )
    parser.add_argument('website', type=str, help='one of these blogs: \n'
                        'travelsmart, bozho, igicheva, pateshestvenik, az_moga')
    parser.add_argument('-c', '--csv', action='store_true', help='export to CSV')
    parser.add_argument('-j', '--json', action='store_true', help='export to JSON')
    parser.add_argument('-n', '--number', type=int, default=20, metavar='', 
                        help='specify the number of articles to scrape')
    parser.add_argument('-f', '--format', action='store_true', help='format the exported data')                 
    #parser.add_argument('-i', '--items', action='store_true', help='Menu for item customization')
    
    return parser.parse_args()


def main(args):
    if args.website in predefined_blogs.keys():
        blog = predefined_blogs[args.website]()
        blog.scrape(args.number)
        
        path = os.path.join(os.path.dirname(__file__), f'output/{args.website}')

        if args.csv:
            blog.export_to_csv(path + '.csv')
    
        if args.json:
            blog.export_to_json(path + '.json')

        if not args.csv and not args.json:
            print(blog.df)
        
        if args.format and not args.csv:
            formatter = DataFormatter()
            formatter.import_file(path + '.json')
            formatter.format()
            formatter.export_to_json(path + '_formatted.json')

    else:
        #TODO: Think of smth smarter
        print("Thats all folks!")
    

if __name__ == "__main__": 
    args = parse_args()
    main(args)