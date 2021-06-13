#!/usr/bin/env python3

from module.web_scraper import WebScraper, Item # pragma: no cover
from module.default_blogs import predefined_blogs
import argparse

def parse_args():  # pragma: no cover
    """Parse the input args."""
    parser = argparse.ArgumentParser(
        description="WebScraper"
    )
    parser.add_argument('website', type=str, help='URL to your favorite blog')
    parser.add_argument('-i', '--items', action='store_true', help='Menu for item customization')
    
    return parser.parse_args()


def main(args):
    if args.website in predefined_blogs.keys():
        predefined_blogs[args.website]()
    else:
        print("We ain't ready for that, mate!")
    

if __name__ == "__main__": 
    args = parse_args()
    main(args)