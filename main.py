#!/usr/bin/env python3

from module.default_blogs import Blog
import argparse


def parse_args():
    """Parse the input args."""
    parser = argparse.ArgumentParser(
        description="WebScraper for WordPress-based blogs."
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

    if args.scrape:
        Blog.scrape_to_file(args.website, args.number)

    if args.format:
        Blog.format_from_file(args.website)

    if not (args.scrape or args.format):
        Blog.scrape_and_format(args.website, args.number)


if __name__ == "__main__": 
    args = parse_args()
    main(args)
