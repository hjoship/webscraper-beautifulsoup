#!/usr/bin/env python3
"""
Web Scraper using Beautiful Soup
A comprehensive web scraping tool with multiple examples and features.
"""

import requests
from bs4 import BeautifulSoup
import csv
import json
import time
import random
from urllib.parse import urljoin, urlparse
from typing import List, Dict, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class WebScraper:
    """A versatile web scraper class using Beautiful Soup."""
    
    def __init__(self, delay_range=(1, 3), headers=None):
        """
        Initialize the web scraper.
        
        Args:
            delay_range (tuple): Range for random delays between requests
            headers (dict): Custom headers for requests
        """
        self.session = requests.Session()
        self.delay_range = delay_range
        
        # Default headers to mimic a real browser
        default_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        
        if headers:
            default_headers.update(headers)
        
        self.session.headers.update(default_headers)
    
    def get_page(self, url: str, timeout: int = 10) -> Optional[BeautifulSoup]:
        """
        Fetch and parse a web page.
        
        Args:
            url (str): URL to scrape
            timeout (int): Request timeout in seconds
            
        Returns:
            BeautifulSoup object or None if failed
        """
        try:
            logger.info(f"Fetching: {url}")
            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()
            
            # Add random delay to be respectful
            delay = random.uniform(*self.delay_range)
            time.sleep(delay)
            
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup
            
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
    
    def extract_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Extract all links from a page."""
        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(base_url, href)
            links.append(full_url)
        return links
    
    def extract_images(self, soup: BeautifulSoup, base_url: str) -> List[Dict[str, str]]:
        """Extract all images from a page."""
        images = []
        for img in soup.find_all('img'):
            src = img.get('src')
            alt = img.get('alt', '')
            if src:
                full_url = urljoin(base_url, src)
                images.append({
                    'src': full_url,
                    'alt': alt,
                    'title': img.get('title', '')
                })
        return images
    
    def extract_text_content(self, soup: BeautifulSoup, selector: str = None) -> str:
        """Extract text content from a page or specific elements."""
        if selector:
            elements = soup.select(selector)
            return ' '.join([elem.get_text(strip=True) for elem in elements])
        else:
            return soup.get_text(strip=True)


class NewsScraper(WebScraper):
    """Specialized scraper for news websites."""
    
    def scrape_articles(self, url: str, article_selector: str, 
                       title_selector: str, content_selector: str) -> List[Dict[str, str]]:
        """
        Scrape articles from a news website.
        
        Args:
            url (str): URL of the news website
            article_selector (str): CSS selector for article containers
            title_selector (str): CSS selector for article titles
            content_selector (str): CSS selector for article content
            
        Returns:
            List of dictionaries containing article data
        """
        soup = self.get_page(url)
        if not soup:
            return []
        
        articles = []
        article_elements = soup.select(article_selector)
        
        for article in article_elements:
            title_elem = article.select_one(title_selector)
            content_elem = article.select_one(content_selector)
            
            title = title_elem.get_text(strip=True) if title_elem else "No title"
            content = content_elem.get_text(strip=True) if content_elem else "No content"
            
            # Extract article URL if available
            link_elem = article.find('a', href=True)
            article_url = urljoin(url, link_elem['href']) if link_elem else ""
            
            articles.append({
                'title': title,
                'content': content,
                'url': article_url,
                'scraped_from': url
            })
        
        return articles


class EcommerceScraper(WebScraper):
    """Specialized scraper for e-commerce websites."""
    
    def scrape_products(self, url: str, product_selector: str,
                       name_selector: str, price_selector: str,
                       image_selector: str = None) -> List[Dict[str, str]]:
        """
        Scrape product information from an e-commerce site.
        
        Args:
            url (str): URL of the product listing page
            product_selector (str): CSS selector for product containers
            name_selector (str): CSS selector for product names
            price_selector (str): CSS selector for product prices
            image_selector (str): CSS selector for product images
            
        Returns:
            List of dictionaries containing product data
        """
        soup = self.get_page(url)
        if not soup:
            return []
        
        products = []
        product_elements = soup.select(product_selector)
        
        for product in product_elements:
            name_elem = product.select_one(name_selector)
            price_elem = product.select_one(price_selector)
            
            name = name_elem.get_text(strip=True) if name_elem else "No name"
            price = price_elem.get_text(strip=True) if price_elem else "No price"
            
            product_data = {
                'name': name,
                'price': price,
                'scraped_from': url
            }
            
            # Extract image URL if selector provided
            if image_selector:
                img_elem = product.select_one(image_selector)
                if img_elem:
                    img_src = img_elem.get('src') or img_elem.get('data-src')
                    if img_src:
                        product_data['image'] = urljoin(url, img_src)
            
            # Extract product URL
            link_elem = product.find('a', href=True)
            if link_elem:
                product_data['url'] = urljoin(url, link_elem['href'])
            
            products.append(product_data)
        
        return products


def save_to_csv(data: List[Dict], filename: str):
    """Save scraped data to CSV file."""
    if not data:
        logger.warning("No data to save")
        return
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    
    logger.info(f"Data saved to {filename}")


def save_to_json(data: List[Dict], filename: str):
    """Save scraped data to JSON file."""
    with open(filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, indent=2, ensure_ascii=False)
    
    logger.info(f"Data saved to {filename}")


def example_basic_scraping():
    """Example of basic web scraping."""
    print("\n=== Basic Web Scraping Example ===")
    
    scraper = WebScraper()
    
    # Example: Scrape quotes from quotes.toscrape.com
    url = "http://quotes.toscrape.com/"
    soup = scraper.get_page(url)
    
    if soup:
        quotes = []
        for quote in soup.find_all('div', class_='quote'):
            text = quote.find('span', class_='text').get_text()
            author = quote.find('small', class_='author').get_text()
            tags = [tag.get_text() for tag in quote.find_all('a', class_='tag')]
            
            quotes.append({
                'text': text,
                'author': author,
                'tags': ', '.join(tags)
            })
        
        print(f"Scraped {len(quotes)} quotes")
        
        # Save to files
        save_to_csv(quotes, 'quotes.csv')
        save_to_json(quotes, 'quotes.json')
        
        # Display first few quotes
        for i, quote in enumerate(quotes[:3]):
            print(f"\nQuote {i+1}:")
            print(f"Text: {quote['text']}")
            print(f"Author: {quote['author']}")
            print(f"Tags: {quote['tags']}")


def example_news_scraping():
    """Example of news website scraping."""
    print("\n=== News Scraping Example ===")
    
    news_scraper = NewsScraper()
    
    # Example selectors (these would need to be adjusted for real news sites)
    url = "https://example-news-site.com"
    articles = news_scraper.scrape_articles(
        url=url,
        article_selector='.article',
        title_selector='.article-title',
        content_selector='.article-summary'
    )
    
    print(f"Would scrape articles from {url}")
    print("Note: Adjust selectors for real news websites")


def example_ecommerce_scraping():
    """Example of e-commerce scraping."""
    print("\n=== E-commerce Scraping Example ===")
    
    ecommerce_scraper = EcommerceScraper()
    
    # Example selectors (these would need to be adjusted for real e-commerce sites)
    url = "https://example-shop.com/products"
    products = ecommerce_scraper.scrape_products(
        url=url,
        product_selector='.product-item',
        name_selector='.product-name',
        price_selector='.product-price',
        image_selector='.product-image img'
    )
    
    print(f"Would scrape products from {url}")
    print("Note: Adjust selectors for real e-commerce websites")


def main():
    """Main function demonstrating various scraping examples."""
    print("Web Scraper with Beautiful Soup")
    print("=" * 40)
    
    # Run basic scraping example
    example_basic_scraping()
    
    # Show other examples (commented out as they need real URLs)
    # example_news_scraping()
    # example_ecommerce_scraping()
    
    print("\n=== Scraping Tips ===")
    print("1. Always check robots.txt before scraping")
    print("2. Be respectful with request frequency")
    print("3. Handle errors gracefully")
    print("4. Use appropriate selectors for target websites")
    print("5. Consider using proxies for large-scale scraping")


if __name__ == "__main__":
    main()