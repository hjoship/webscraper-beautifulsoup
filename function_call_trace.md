# Detailed Function Call Trace

## Complete Function Call Hierarchy

### webscraper.py Main Execution Flow

```
if __name__ == "__main__":
    main()
    │
    ├── print() statements
    ├── example_basic_scraping()
    │   │
    │   ├── WebScraper() ──────────────────┐
    │   │   │                              │
    │   │   └── __init__(delay_range, headers)
    │   │       ├── requests.Session()
    │   │       └── session.headers.update()
    │   │
    │   ├── scraper.get_page(url) ◄─────────┤
    │   │   │                              │
    │   │   ├── logger.info()              │
    │   │   ├── session.get(url, timeout)  │
    │   │   ├── response.raise_for_status() │
    │   │   ├── random.uniform()           │
    │   │   ├── time.sleep()               │
    │   │   ├── BeautifulSoup(content)     │
    │   │   └── return soup                │
    │   │
    │   ├── soup.find_all('div', class_='quote')
    │   ├── quote.find('span', class_='text')
    │   ├── quote.find('small', class_='author')
    │   ├── quote.find_all('a', class_='tag')
    │   ├── save_to_csv(quotes, 'quotes.csv')
    │   │   │
    │   │   ├── csv.DictWriter()
    │   │   ├── writer.writeheader()
    │   │   ├── writer.writerows()
    │   │   └── logger.info()
    │   │
    │   ├── save_to_json(quotes, 'quotes.json')
    │   │   │
    │   │   ├── json.dump()
    │   │   └── logger.info()
    │   │
    │   └── print() statements
    │
    ├── example_news_scraping()
    │   │
    │   ├── NewsScraper() ─────────────────┐
    │   │   │                             │
    │   │   └── __init__() ◄──────────────┤ (inherits from WebScraper)
    │   │                                 │
    │   └── news_scraper.scrape_articles() │
    │       │                             │
    │       ├── self.get_page(url) ◄──────┘
    │       ├── soup.select(article_selector)
    │       ├── article.select_one(title_selector)
    │       ├── article.select_one(content_selector)
    │       ├── article.find('a', href=True)
    │       ├── urljoin(url, href)
    │       └── return articles
    │
    └── example_ecommerce_scraping()
        │
        ├── EcommerceScraper() ───────────┐
        │   │                            │
        │   └── __init__() ◄─────────────┤ (inherits from WebScraper)
        │                                │
        └── ecommerce_scraper.scrape_products()
            │                            │
            ├── self.get_page(url) ◄─────┘
            ├── soup.select(product_selector)
            ├── product.select_one(name_selector)
            ├── product.select_one(price_selector)
            ├── product.select_one(image_selector)
            ├── product.find('a', href=True)
            ├── urljoin(url, href)
            └── return products
```

### examples.py Execution Flow

```
if __name__ == "__main__":
    main()
    │
    ├── scrape_wikipedia_table()
    │   │
    │   ├── WebScraper() ──────────────────┐
    │   ├── scraper.get_page(url) ◄────────┤
    │   ├── soup.find('table', class_='wikitable')
    │   ├── table.find_all('tr')[1:]
    │   ├── row.find_all(['td', 'th'])
    │   ├── cells[0].get_text(strip=True)
    │   ├── cells[1].get_text(strip=True)
    │   ├── cells[2].get_text(strip=True)
    │   └── save_to_csv(countries, filename)
    │
    ├── scrape_github_trending()
    │   │
    │   ├── WebScraper() ──────────────────┐
    │   ├── scraper.get_page(url) ◄────────┤
    │   ├── soup.find_all('article', class_='Box-row')
    │   ├── repo.find('h2', class_='h3')
    │   ├── title_elem.find('a')
    │   ├── repo.find('p', class_='col-9')
    │   ├── repo.find('span', {'itemprop': 'programmingLanguage'})
    │   ├── repo.find('a', href=lambda x: x and '/stargazers' in x)
    │   └── save_to_json(repos, filename)
    │
    ├── scrape_news_headlines()
    │   │
    │   ├── WebScraper() ──────────────────┐
    │   ├── scraper.get_page(url) ◄────────┤
    │   ├── soup.select(selector) [for each selector]
    │   ├── elem.get_text(strip=True)
    │   ├── elem.find('a')
    │   └── save_to_csv(headlines, filename)
    │
    └── custom_scraping_example()
        │
        ├── WebScraper(delay_range=(1, 2))
        └── scraper.get_page(url) ◄───────┘
```

## Class Method Call Chains

### WebScraper Class Methods

```
WebScraper.__init__(delay_range, headers)
├── requests.Session()
├── default_headers = {...}
├── headers.update() [if custom headers]
└── session.headers.update()

WebScraper.get_page(url, timeout)
├── logger.info(f"Fetching: {url}")
├── session.get(url, timeout=timeout)
├── response.raise_for_status()
├── random.uniform(*self.delay_range)
├── time.sleep(delay)
├── BeautifulSoup(response.content, 'html.parser')
└── return soup
│
├── [Exception Handler]
│   ├── logger.error(f"Error fetching {url}: {e}")
│   └── return None

WebScraper.extract_links(soup, base_url)
├── soup.find_all('a', href=True)
├── urljoin(base_url, href) [for each link]
└── return links

WebScraper.extract_images(soup, base_url)
├── soup.find_all('img')
├── img.get('src')
├── img.get('alt', '')
├── img.get('title', '')
├── urljoin(base_url, src)
└── return images

WebScraper.extract_text_content(soup, selector)
├── [if selector provided]
│   ├── soup.select(selector)
│   └── elem.get_text(strip=True) [for each element]
├── [else]
│   └── soup.get_text(strip=True)
└── return text
```

### NewsScraper Class Methods

```
NewsScraper.scrape_articles(url, article_selector, title_selector, content_selector)
├── self.get_page(url) ──────────┐
├── [if not soup] return []      │
├── soup.select(article_selector)│
├── [for each article]           │
│   ├── article.select_one(title_selector)
│   ├── article.select_one(content_selector)
│   ├── title_elem.get_text(strip=True)
│   ├── content_elem.get_text(strip=True)
│   ├── article.find('a', href=True)
│   └── urljoin(url, link_elem['href'])
└── return articles              │
                                 │
Inherits from WebScraper ◄───────┘
├── __init__()
├── get_page()
├── extract_links()
├── extract_images()
└── extract_text_content()
```

### EcommerceScraper Class Methods

```
EcommerceScraper.scrape_products(url, product_selector, name_selector, price_selector, image_selector)
├── self.get_page(url) ──────────┐
├── [if not soup] return []      │
├── soup.select(product_selector)│
├── [for each product]           │
│   ├── product.select_one(name_selector)
│   ├── product.select_one(price_selector)
│   ├── name_elem.get_text(strip=True)
│   ├── price_elem.get_text(strip=True)
│   ├── [if image_selector]
│   │   ├── product.select_one(image_selector)
│   │   ├── img_elem.get('src') or img_elem.get('data-src')
│   │   └── urljoin(url, img_src)
│   ├── product.find('a', href=True)
│   └── urljoin(url, link_elem['href'])
└── return products              │
                                 │
Inherits from WebScraper ◄───────┘
├── __init__()
├── get_page()
├── extract_links()
├── extract_images()
└── extract_text_content()
```

## Utility Functions Call Chain

```
save_to_csv(data, filename)
├── [if not data] logger.warning() & return
├── open(filename, 'w', newline='', encoding='utf-8')
├── csv.DictWriter(csvfile, fieldnames=data[0].keys())
├── writer.writeheader()
├── writer.writerows(data)
└── logger.info(f"Data saved to {filename}")

save_to_json(data, filename)
├── open(filename, 'w', encoding='utf-8')
├── json.dump(data, jsonfile, indent=2, ensure_ascii=False)
└── logger.info(f"Data saved to {filename}")
```

## External Library Function Calls

```
requests Library:
├── requests.Session()
├── session.get(url, timeout=timeout)
├── session.headers.update(headers)
└── response.raise_for_status()

BeautifulSoup Library:
├── BeautifulSoup(content, 'html.parser')
├── soup.find_all(tag, attributes)
├── soup.find(tag, attributes)
├── soup.select(css_selector)
├── soup.select_one(css_selector)
├── element.get_text(strip=True)
├── element.get(attribute_name)
└── element.get(attribute_name, default_value)

Standard Library:
├── time.sleep(seconds)
├── random.uniform(min, max)
├── logging.basicConfig()
├── logger.info() / logger.error() / logger.warning()
├── csv.DictWriter()
├── json.dump()
├── urllib.parse.urljoin()
└── urllib.parse.urlparse()
```

## Error Handling Call Stack

```
WebScraper.get_page()
├── try:
│   ├── session.get() ──────────┐
│   ├── response.raise_for_status()
│   ├── BeautifulSoup()         │
│   └── return soup             │
└── except requests.RequestException as e:
    ├── logger.error() ◄────────┘
    └── return None

Main Functions
├── [Check if soup is None]
├── [if soup:] continue processing
└── [else:] handle gracefully
```

This architecture shows that the system follows a clear hierarchy where:
1. **Base WebScraper** provides core functionality
2. **Specialized scrapers** inherit and extend base functionality  
3. **Example functions** demonstrate usage patterns
4. **Utility functions** handle data export
5. **Error handling** is built into each layer