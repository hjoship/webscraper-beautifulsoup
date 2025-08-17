# Web Scraper Architecture Diagram

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        WEB SCRAPER SYSTEM                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────┐    ┌─────────────────┐    ┌──────────────┐ │
│  │   examples.py   │    │  webscraper.py  │    │  config.json │ │
│  │   (Examples)    │    │   (Core Logic)  │    │ (Settings)   │ │
│  └─────────────────┘    └─────────────────┘    └──────────────┘ │
│           │                       │                     │       │
│           └───────────────────────┼─────────────────────┘       │
│                                   │                             │
│                          ┌────────▼────────┐                    │
│                          │  Beautiful Soup │                    │
│                          │   + Requests    │                    │
│                          └─────────────────┘                    │
│                                   │                             │
│                          ┌────────▼────────┐                    │
│                          │   Web Sources   │                    │
│                          │ (quotes, wiki,  │                    │
│                          │  github, etc.)  │                    │
│                          └─────────────────┘                    │
└─────────────────────────────────────────────────────────────────┘
```

## Class Hierarchy and Function Calls

```
WebScraper (Base Class)
├── __init__(delay_range, headers)
├── get_page(url, timeout) ──────────┐
│   ├── requests.Session.get()       │
│   ├── BeautifulSoup()              │
│   └── time.sleep()                 │
├── extract_links(soup, base_url)    │
├── extract_images(soup, base_url)   │
└── extract_text_content(soup)       │
                                     │
NewsScraper (Inherits WebScraper)    │
├── scrape_articles() ───────────────┤
│   ├── get_page() ◄──────────────────┘
│   ├── soup.select()
│   └── urljoin()
│
EcommerceScraper (Inherits WebScraper)
├── scrape_products() ───────────────┐
│   ├── get_page() ◄──────────────────┘
│   ├── soup.select()
│   └── urljoin()
│
Utility Functions
├── save_to_csv(data, filename)
│   └── csv.DictWriter()
├── save_to_json(data, filename)
│   └── json.dump()
└── logging functions
```

## Function Call Flow Diagram

```
main() [webscraper.py]
│
├── example_basic_scraping()
│   ├── WebScraper() ──────────────┐
│   │   └── __init__()             │
│   ├── scraper.get_page() ◄───────┤
│   │   ├── session.get()          │
│   │   ├── BeautifulSoup()        │
│   │   └── time.sleep()           │
│   ├── soup.find_all()            │
│   ├── save_to_csv() ─────────────┤
│   │   └── csv.DictWriter()       │
│   └── save_to_json() ────────────┤
│       └── json.dump()            │
│                                  │
├── example_news_scraping()        │
│   └── NewsScraper() ─────────────┤
│       └── scrape_articles() ◄───┤
│           └── get_page() ◄───────┘
│
└── example_ecommerce_scraping()
    └── EcommerceScraper() ───────┐
        └── scrape_products() ◄──┤
            └── get_page() ◄──────┘
```

## Examples.py Function Call Flow

```
main() [examples.py]
│
├── scrape_wikipedia_table()
│   ├── WebScraper() ─────────────┐
│   ├── scraper.get_page() ◄──────┤
│   ├── soup.find() ──────────────┤
│   ├── soup.find_all()           │
│   └── save_to_csv() ────────────┤
│                                 │
├── scrape_github_trending()      │
│   ├── WebScraper() ─────────────┤
│   ├── scraper.get_page() ◄──────┤
│   ├── soup.find_all()           │
│   └── save_to_json() ───────────┤
│                                 │
├── scrape_news_headlines()       │
│   ├── WebScraper() ─────────────┤
│   ├── scraper.get_page() ◄──────┤
│   ├── soup.select()             │
│   └── save_to_csv() ────────────┤
│                                 │
└── custom_scraping_example()     │
    ├── WebScraper() ─────────────┘
    └── scraper.get_page() ◄──────┐
                                  │
Common Utility Functions ◄────────┘
├── save_to_csv()
├── save_to_json()
└── logging functions
```

## Data Flow Architecture

```
┌─────────────┐    ┌──────────────┐    ┌─────────────────┐
│   Input     │    │  Processing  │    │     Output      │
│             │    │              │    │                 │
│ ┌─────────┐ │    │ ┌──────────┐ │    │ ┌─────────────┐ │
│ │   URL   │ │───▶│ │get_page()│ │───▶│ │BeautifulSoup│ │
│ └─────────┘ │    │ └──────────┘ │    │ │   Object    │ │
│             │    │              │    │ └─────────────┘ │
│ ┌─────────┐ │    │ ┌──────────┐ │    │        │        │
│ │Selectors│ │───▶│ │ Parsing  │ │    │        ▼        │
│ └─────────┘ │    │ │Functions │ │    │ ┌─────────────┐ │
│             │    │ └──────────┘ │    │ │ Extracted   │ │
│ ┌─────────┐ │    │              │    │ │    Data     │ │
│ │ Config  │ │───▶│ ┌──────────┐ │    │ └─────────────┘ │
│ └─────────┘ │    │ │Error     │ │    │        │        │
└─────────────┘    │ │Handling  │ │    │        ▼        │
                   │ └──────────┘ │    │ ┌─────────────┐ │
                   └──────────────┘    │ │   CSV/JSON  │ │
                                       │ │    Files    │ │
                                       │ └─────────────┘ │
                                       └─────────────────┘
```

## Dependency Graph

```
External Dependencies:
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  requests   │    │beautifulsoup4│    │    lxml     │
│             │    │             │    │             │
│ ┌─────────┐ │    │ ┌─────────┐ │    │ ┌─────────┐ │
│ │Session  │ │    │ │BeautifulSoup│    │ │XML/HTML │ │
│ │.get()   │ │    │ │.find()  │ │    │ │ Parser  │ │
│ │.headers │ │    │ │.select()│ │    │ └─────────┘ │
│ └─────────┘ │    │ └─────────┘ │    └─────────────┘
└─────────────┘    └─────────────┘
       │                   │
       └─────────┬─────────┘
                 │
        ┌────────▼────────┐
        │   webscraper.py │
        │                 │
        │ ┌─────────────┐ │
        │ │ WebScraper  │ │
        │ │   Class     │ │
        │ └─────────────┘ │
        │        │        │
        │        ▼        │
        │ ┌─────────────┐ │
        │ │NewsScraper  │ │
        │ │EcommerceScraper│
        │ └─────────────┘ │
        └─────────────────┘
                 │
        ┌────────▼────────┐
        │   examples.py   │
        │                 │
        │ ┌─────────────┐ │
        │ │ Specific    │ │
        │ │ Use Cases   │ │
        │ └─────────────┘ │
        └─────────────────┘
```

## Method Interaction Matrix

| Class/Function | get_page() | find_all() | select() | save_to_csv() | save_to_json() |
|----------------|------------|------------|----------|---------------|----------------|
| WebScraper     | ✓ Defines  | Uses       | Uses     | Uses          | Uses           |
| NewsScraper    | ✓ Inherits | Uses       | Uses     | Uses          | Uses           |
| EcommerceScraper| ✓ Inherits| Uses       | Uses     | Uses          | Uses           |
| examples.py    | ✓ Calls    | Uses       | Uses     | ✓ Calls       | ✓ Calls        |

## Error Handling Flow

```
User Request
     │
     ▼
┌─────────────┐
│ get_page()  │
└─────────────┘
     │
     ▼
┌─────────────┐    ┌─────────────┐
│ try block   │───▶│ requests.   │
│             │    │ get()       │
└─────────────┘    └─────────────┘
     │                    │
     ▼                    ▼
┌─────────────┐    ┌─────────────┐
│ Success?    │◄───│ Response    │
└─────────────┘    │ Status      │
     │             └─────────────┘
     ▼
┌─────────────┐    ┌─────────────┐
│ Return Soup │    │ Log Error & │
│ Object      │    │ Return None │
└─────────────┘    └─────────────┘
```

## Key Design Patterns Used

1. **Inheritance Pattern**: NewsScraper and EcommerceScraper inherit from WebScraper
2. **Template Method Pattern**: Base scraping logic in parent, specific implementations in children
3. **Factory Pattern**: Different scraper types for different website categories
4. **Strategy Pattern**: Different parsing strategies for different content types
5. **Observer Pattern**: Logging system observes and reports scraping activities

## Configuration Flow

```
config.json
     │
     ▼
┌─────────────┐
│ Load Config │
└─────────────┘
     │
     ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Headers     │    │ Delays      │    │ Selectors   │
│ Settings    │    │ Settings    │    │ Settings    │
└─────────────┘    └─────────────┘    └─────────────┘
     │                    │                    │
     └────────────────────┼────────────────────┘
                          │
                          ▼
                 ┌─────────────┐
                 │ WebScraper  │
                 │ Instance    │
                 └─────────────┘
```