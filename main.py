#!/usr/bin/env python3

from module.default_blogs import Blog
from module.data_handler import DataHandler
import argparse
import os


def parse_args():
    """Parse the input args."""
    parser = argparse.ArgumentParser(
        description="WebScraper"
    )
    parser.add_argument('website', type=str, help='one of these blogs: \n'
                        'travelsmart, bozho, igicheva, pateshestvenik, az_moga')
    parser.add_argument('-s', '--scrape', action='store_true', help='scrape POSTS number of articles')
    parser.add_argument('-n', '--number', type=int, default=20, metavar='POSTS',
                        help='specify the number of articles to scrape')
    parser.add_argument('-f', '--format', action='store_true', help='format the exported data')
    
    return parser.parse_args()


def main(args):
    if Blog.not_supported(args.website):
        print(f"We are unable to scrape {args.website}.")
        print("Run with -h to see valid arguments.")
        exit(1)

    path = os.path.join(os.path.dirname(__file__), f'output/{args.website}')

    if args.scrape:
        try:
            scraper = Blog.scraper(args.website)
            scraper.scrape(args.number)
            DataHandler.data_frame_to_json(scraper.df, path + '.json')
        except PermissionError:
            print(f"Access denied. Failed to write {args.website}.json.")

    if args.format:
        try:
            formatter = Blog.formatter(args.website)
            result = formatter.format(DataHandler.json_to_obj(path + '.json'))
            DataHandler.obj_to_json(result, path + '_formatted.json')
        except FileNotFoundError:
            print(f"No data to format. {args.website}.json not found in output/ dir.")
            exit(2)
        except PermissionError:
            print(f"Access denied. Failed to write {args.website}_formatted.json.")
            exit(3)

if __name__ == "__main__": 
    args = parse_args()
    main(args)
