# Web Scraper for WordPress-based Blogs

#### By _Julia, Kiril, Martina,_ and _Nikolay_
<br>

## Usage:
### Scraper and Formatter:
- Run `main.py` with the name of a supported `website`.
- To scrape the website to a json, run with `-s`/`--scrape`.
- To format scraped data to a json, run with `-f`/`--format`.
- Run _without_ `-s` and `-f` to scrape and save __only formatted__ data.
- Specify the number of articles to scrape with `-n NUM`.
### Web App:
- `web_instance.py` starts a debug server with all previously scraped data.
- `run.sh`:
  - scrapes our primary supported blog (travelsmart),
  - starts a server and opens it in the default browser,
  - proceeds to scrape all supported blogs.<br>

  _Newly scraped data is automatically loaded in. <br>
  An argument may be passed to specify the number of posts to scrape from each blog._

<br>

### Supported blogs:
1. [`travelsmart`](https://www.travelsmart.bg/)
2. [`bozho`](https://blog.bozho.net/)
3. [`igicheva`](https://igicheva.wordpress.com/)
4. [`pateshestvenik`](https://pateshestvenik.com/)
5. [`az_moga`](https://az-moga.com/)

<br>

## Task
Web scraper - automatically gather info from selected websites (blogs):
1. Develop a scraper using a Test Driven Development process.
1. Process the data for subsequent usage (storage/access/search).
1. Present the data through a simple frontend.
