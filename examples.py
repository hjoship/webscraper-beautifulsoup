#!/usr/bin/env python3
"""
Simple Web Scraper Examples
Quick examples for common scraping tasks.
"""

from webscraper import WebScraper, save_to_csv, save_to_json
import requests
from bs4 import BeautifulSoup


def scrape_wikipedia_table():
    """Example: Scrape a table from Wikipedia."""
    print("Scraping Wikipedia table example...")
    
    scraper = WebScraper()
    url = "https://en.wikipedia.org/wiki/List_of_countries_by_population"
    
    soup = scraper.get_page(url)
    if not soup:
        print("Failed to fetch the page")
        return
    
    # Find the first table with class 'wikitable'
    table = soup.find('table', class_='wikitable')
    if not table:
        print("No table found")
        return
    
    countries = []
    rows = table.find_all('tr')[1:]  # Skip header row
    
    for row in rows[:10]:  # Get first 10 countries
        cells = row.find_all(['td', 'th'])
        if len(cells) >= 3:
            rank = cells[0].get_text(strip=True)
            country = cells[1].get_text(strip=True)
            population = cells[2].get_text(strip=True)
            
            countries.append({
                'rank': rank,
                'country': country,
                'population': population
            })
    
    print(f"Scraped {len(countries)} countries")
    save_to_csv(countries, 'countries_population.csv')
    
    # Display results
    for country in countries[:5]:
        print(f"{country['rank']}. {country['country']}: {country['population']}")


def scrape_github_trending():
    """Example: Scrape GitHub trending repositories."""
    print("\nScraping GitHub trending repositories...")
    
    scraper = WebScraper()
    url = "https://github.com/trending"
    
    soup = scraper.get_page(url)
    if not soup:
        print("Failed to fetch GitHub trending page")
        return
    
    repos = []
    repo_elements = soup.find_all('article', class_='Box-row')
    
    for repo in repo_elements[:5]:  # Get first 5 repos
        # Extract repository name
        title_elem = repo.find('h2', class_='h3')
        if title_elem:
            repo_link = title_elem.find('a')
            if repo_link:
                repo_name = repo_link.get_text(strip=True)
                repo_url = "https://github.com" + repo_link['href']
                
                # Extract description
                desc_elem = repo.find('p', class_='col-9')
                description = desc_elem.get_text(strip=True) if desc_elem else "No description"
                
                # Extract language
                lang_elem = repo.find('span', {'itemprop': 'programmingLanguage'})
                language = lang_elem.get_text(strip=True) if lang_elem else "Unknown"
                
                # Extract stars
                stars_elem = repo.find('a', href=lambda x: x and '/stargazers' in x)
                stars = stars_elem.get_text(strip=True) if stars_elem else "0"
                
                repos.append({
                    'name': repo_name,
                    'url': repo_url,
                    'description': description,
                    'language': language,
                    'stars': stars
                })
    
    print(f"Scraped {len(repos)} trending repositories")
    save_to_json(repos, 'github_trending.json')
    
    # Display results
    for repo in repos:
        print(f"\n{repo['name']}")
        print(f"Language: {repo['language']}")
        print(f"Stars: {repo['stars']}")
        print(f"Description: {repo['description'][:100]}...")


def scrape_news_headlines():
    """Example: Scrape news headlines from a news aggregator."""
    print("\nScraping news headlines example...")
    
    scraper = WebScraper()
    
    # Using a simple news site for demonstration
    url = "https://lite.cnn.com"
    
    soup = scraper.get_page(url)
    if not soup:
        print("Failed to fetch news page")
        return
    
    headlines = []
    
    # Look for common headline selectors
    headline_selectors = ['h1', 'h2', 'h3', '.headline', '.title']
    
    for selector in headline_selectors:
        elements = soup.select(selector)
        for elem in elements[:5]:  # Limit to 5 per selector
            text = elem.get_text(strip=True)
            if len(text) > 20:  # Filter out short text
                link = elem.find('a')
                headline_url = ""
                if link and link.get('href'):
                    headline_url = link['href']
                    if not headline_url.startswith('http'):
                        headline_url = f"https://lite.cnn.com{headline_url}"
                
                headlines.append({
                    'headline': text,
                    'url': headline_url,
                    'source': 'CNN Lite'
                })
        
        if headlines:  # If we found headlines, break
            break
    
    # Remove duplicates
    seen = set()
    unique_headlines = []
    for headline in headlines:
        if headline['headline'] not in seen:
            seen.add(headline['headline'])
            unique_headlines.append(headline)
    
    print(f"Scraped {len(unique_headlines)} unique headlines")
    save_to_csv(unique_headlines, 'news_headlines.csv')
    
    # Display results
    for headline in unique_headlines[:5]:
        print(f"\n• {headline['headline']}")


def custom_scraping_example():
    """Template for custom scraping tasks."""
    print("\nCustom scraping template...")
    
    # Initialize scraper
    scraper = WebScraper(delay_range=(1, 2))
    
    # Your target URL
    url = "https://example.com"
    
    # Get the page
    soup = scraper.get_page(url)
    if not soup:
        print("Failed to fetch the page")
        return
    
    # Extract data using CSS selectors or find methods
    # Example:
    # titles = soup.select('.title')
    # prices = soup.select('.price')
    # images = soup.select('img.product-image')
    
    # Process and save data
    data = []
    # for title, price in zip(titles, prices):
    #     data.append({
    #         'title': title.get_text(strip=True),
    #         'price': price.get_text(strip=True)
    #     })
    
    # save_to_csv(data, 'custom_data.csv')
    
    print("Custom scraping template ready - modify as needed!")


if __name__ == "__main__":
    print("Web Scraper Examples")
    print("=" * 30)
    
    try:
        # Run examples
        scrape_wikipedia_table()
        scrape_github_trending()
        scrape_news_headlines()
        custom_scraping_example()
        
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Make sure you have installed the required packages:")
        print("pip install -r requirements.txt")