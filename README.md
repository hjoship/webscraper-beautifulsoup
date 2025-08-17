# Web Scraper with Beautiful Soup

A comprehensive Python web scraping toolkit using Beautiful Soup, designed for various scraping tasks with built-in best practices.

## Features

- **Respectful scraping** with random delays between requests
- **Error handling** and logging
- **Multiple scraper classes** for different use cases
- **Data export** to CSV and JSON formats
- **Browser-like headers** to avoid blocking
- **Modular design** for easy customization

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

### Basic Usage

```python
from webscraper import WebScraper

# Initialize scraper
scraper = WebScraper()

# Scrape a page
soup = scraper.get_page("https://example.com")

# Extract data
titles = soup.find_all('h1')
for title in titles:
    print(title.get_text())
```

### Run Examples

```bash
# Run the main scraper with built-in examples
python webscraper.py

# Run specific examples
python examples.py
```

## Available Classes

### WebScraper (Base Class)
- Basic web scraping functionality
- Handles requests, delays, and parsing
- Methods for extracting links, images, and text

### NewsScraper
- Specialized for news websites
- Extracts articles with titles and content
- Configurable CSS selectors

### EcommerceScraper
- Designed for e-commerce sites
- Extracts product information
- Handles names, prices, and images

## Example Use Cases

### 1. Scraping Quotes
```python
from webscraper import WebScraper, save_to_csv

scraper = WebScraper()
soup = scraper.get_page("http://quotes.toscrape.com/")

quotes = []
for quote in soup.find_all('div', class_='quote'):
    text = quote.find('span', class_='text').get_text()
    author = quote.find('small', class_='author').get_text()
    quotes.append({'text': text, 'author': author})

save_to_csv(quotes, 'quotes.csv')
```

### 2. Scraping Product Information
```python
from webscraper import EcommerceScraper

scraper = EcommerceScraper()
products = scraper.scrape_products(
    url="https://example-shop.com",
    product_selector=".product",
    name_selector=".product-name",
    price_selector=".price"
)
```

### 3. Scraping News Articles
```python
from webscraper import NewsScraper

scraper = NewsScraper()
articles = scraper.scrape_articles(
    url="https://news-site.com",
    article_selector=".article",
    title_selector=".title",
    content_selector=".content"
)
```

## Configuration Options

### Custom Headers
```python
headers = {
    'User-Agent': 'Your Custom User Agent',
    'Accept': 'text/html,application/xhtml+xml'
}
scraper = WebScraper(headers=headers)
```

### Delay Settings
```python
# Random delay between 2-5 seconds
scraper = WebScraper(delay_range=(2, 5))
```

## Best Practices

1. **Check robots.txt** before scraping any website
2. **Be respectful** with request frequency
3. **Handle errors gracefully** with try-catch blocks
4. **Use appropriate selectors** for your target websites
5. **Test selectors** on small samples first
6. **Save data incrementally** for large scraping jobs

## Common CSS Selectors

| Element | Selector Example |
|---------|------------------|
| Class | `.classname` |
| ID | `#idname` |
| Tag | `div`, `p`, `h1` |
| Attribute | `[href]`, `[class="example"]` |
| Descendant | `.parent .child` |
| Direct child | `.parent > .child` |

## Error Handling

The scraper includes built-in error handling for:
- Network timeouts
- HTTP errors (404, 500, etc.)
- Parsing errors
- Missing elements

## Data Export

### CSV Export
```python
save_to_csv(data, 'output.csv')
```

### JSON Export
```python
save_to_json(data, 'output.json')
```

## Legal and Ethical Considerations

- Always respect robots.txt
- Don't overload servers with requests
- Check website terms of service
- Consider rate limiting for large-scale scraping
- Be aware of copyright and data protection laws

## Troubleshooting

### Common Issues

1. **403 Forbidden**: Try different User-Agent headers
2. **Timeout errors**: Increase timeout or add delays
3. **Empty results**: Check CSS selectors on the actual page
4. **Encoding issues**: Specify encoding when saving files

### Debugging Tips

1. Print the HTML to see the actual structure
2. Use browser developer tools to find correct selectors
3. Test selectors in the browser console first
4. Check if content is loaded dynamically (may need Selenium)

## Dependencies

- `requests`: HTTP library for making requests
- `beautifulsoup4`: HTML/XML parser
- `lxml`: Fast XML and HTML parser

## License

This project is open source and available under the MIT License.