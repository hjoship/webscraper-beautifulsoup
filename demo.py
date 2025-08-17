#!/usr/bin/env python3
"""
Demo script showing how to use the web scraper programmatically
and generate visualizations similar to the Streamlit app.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from webscraper import WebScraper
import json
from datetime import datetime

def demo_quotes_scraping():
    """Demo scraping quotes and creating visualizations"""
    print("🕷️ Demo: Scraping Quotes")
    print("=" * 40)
    
    scraper = WebScraper()
    url = "http://quotes.toscrape.com/"
    soup = scraper.get_page(url)
    
    if not soup:
        print("❌ Failed to scrape the website")
        return
    
    quotes = []
    for quote in soup.find_all('div', class_='quote'):
        text = quote.find('span', class_='text').get_text()
        author = quote.find('small', class_='author').get_text()
        tags = [tag.get_text() for tag in quote.find_all('a', class_='tag')]
        
        quotes.append({
            'text': text,
            'author': author,
            'tags': ', '.join(tags),
            'length': len(text),
            'word_count': len(text.split())
        })
    
    print(f"✅ Scraped {len(quotes)} quotes")
    
    # Create DataFrame
    df = pd.DataFrame(quotes)
    
    # Display statistics
    print(f"\n📊 Statistics:")
    print(f"   • Total quotes: {len(df)}")
    print(f"   • Unique authors: {df['author'].nunique()}")
    print(f"   • Average length: {df['length'].mean():.0f} characters")
    print(f"   • Average words: {df['word_count'].mean():.0f} words")
    
    # Show top authors
    print(f"\n👥 Top Authors:")
    top_authors = df['author'].value_counts().head(3)
    for author, count in top_authors.items():
        print(f"   • {author}: {count} quotes")
    
    # Create visualizations (save as HTML)
    print(f"\n📈 Creating visualizations...")
    
    # Quote length distribution
    fig1 = px.histogram(df, x='length', title="Quote Length Distribution")
    fig1.write_html("quote_lengths.html")
    
    # Author quote counts
    author_counts = df['author'].value_counts().head(10)
    fig2 = px.bar(x=author_counts.index, y=author_counts.values, 
                  title="Top 10 Authors by Quote Count")
    fig2.write_html("author_counts.html")
    
    # Word count vs character count
    fig3 = px.scatter(df, x='word_count', y='length', hover_data=['author'],
                      title="Word Count vs Character Count")
    fig3.write_html("word_vs_char.html")
    
    print("   ✅ Saved visualizations as HTML files")
    
    # Save data
    df.to_csv('demo_quotes.csv', index=False)
    df.to_json('demo_quotes.json', orient='records', indent=2)
    print("   ✅ Saved data as CSV and JSON")
    
    return df

def demo_general_scraping():
    """Demo scraping general website content"""
    print("\n🕷️ Demo: Scraping General Content")
    print("=" * 40)
    
    scraper = WebScraper()
    url = "https://en.wikipedia.org/wiki/Web_scraping"
    soup = scraper.get_page(url)
    
    if not soup:
        print("❌ Failed to scrape the website")
        return
    
    # Extract headings
    headings = []
    for i in range(1, 7):
        for heading in soup.find_all(f'h{i}'):
            headings.append({
                'level': i,
                'text': heading.get_text(strip=True),
                'length': len(heading.get_text(strip=True))
            })
    
    # Extract links
    links = scraper.extract_links(soup, url)
    internal_links = [link for link in links if 'wikipedia.org' in link]
    external_links = [link for link in links if 'wikipedia.org' not in link]
    
    # Extract images
    images = scraper.extract_images(soup, url)
    
    print(f"✅ Scraped content from {url}")
    print(f"\n📊 Content Summary:")
    print(f"   • Headings: {len(headings)}")
    print(f"   • Links: {len(links)} (Internal: {len(internal_links)}, External: {len(external_links)})")
    print(f"   • Images: {len(images)}")
    
    # Heading level distribution
    if headings:
        headings_df = pd.DataFrame(headings)
        print(f"\n📝 Heading Levels:")
        level_counts = headings_df['level'].value_counts().sort_index()
        for level, count in level_counts.items():
            print(f"   • H{level}: {count} headings")
        
        # Create heading visualization
        fig = px.histogram(headings_df, x='level', title="Heading Level Distribution")
        fig.write_html("heading_levels.html")
        print("   ✅ Saved heading visualization")
    
    # Create content overview
    content_data = {
        'Content Type': ['Headings', 'Internal Links', 'External Links', 'Images'],
        'Count': [len(headings), len(internal_links), len(external_links), len(images)]
    }
    
    fig = px.pie(values=content_data['Count'], names=content_data['Content Type'],
                 title="Content Distribution")
    fig.write_html("content_distribution.html")
    print("   ✅ Saved content distribution chart")
    
    return {
        'headings': headings,
        'links': {'internal': internal_links, 'external': external_links},
        'images': images
    }

def demo_comparison():
    """Demo comparing multiple websites"""
    print("\n🕷️ Demo: Website Comparison")
    print("=" * 40)
    
    urls = [
        "http://quotes.toscrape.com/",
        "https://en.wikipedia.org/wiki/Python_(programming_language)",
        "https://github.com/trending"
    ]
    
    scraper = WebScraper()
    comparison_data = []
    
    for url in urls:
        print(f"Scraping: {url}")
        soup = scraper.get_page(url)
        
        if soup:
            # Count different elements
            headings = len(soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']))
            links = len(soup.find_all('a', href=True))
            images = len(soup.find_all('img'))
            paragraphs = len(soup.find_all('p'))
            
            comparison_data.append({
                'Website': url.split('/')[2],  # Extract domain
                'Headings': headings,
                'Links': links,
                'Images': images,
                'Paragraphs': paragraphs
            })
    
    if comparison_data:
        df = pd.DataFrame(comparison_data)
        print(f"\n📊 Website Comparison:")
        print(df.to_string(index=False))
        
        # Create comparison chart
        fig = px.bar(df, x='Website', y=['Headings', 'Links', 'Images', 'Paragraphs'],
                     title="Website Content Comparison", barmode='group')
        fig.write_html("website_comparison.html")
        print("\n   ✅ Saved comparison chart")
        
        df.to_csv('website_comparison.csv', index=False)
        print("   ✅ Saved comparison data")

def main():
    """Run all demos"""
    print("🚀 Web Scraper Demo Suite")
    print("=" * 50)
    
    try:
        # Run demos
        quotes_data = demo_quotes_scraping()
        general_data = demo_general_scraping()
        demo_comparison()
        
        print(f"\n🎉 Demo completed successfully!")
        print(f"\n📁 Generated files:")
        print("   • quote_lengths.html")
        print("   • author_counts.html") 
        print("   • word_vs_char.html")
        print("   • heading_levels.html")
        print("   • content_distribution.html")
        print("   • website_comparison.html")
        print("   • demo_quotes.csv/json")
        print("   • website_comparison.csv")
        
        print(f"\n💡 Tips:")
        print("   • Open HTML files in your browser to view charts")
        print("   • Use CSV files for further analysis")
        print("   • Run the Streamlit app for interactive experience:")
        print("     uv run streamlit run streamlit_app.py")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        print("Make sure you have internet connection and required packages installed.")

if __name__ == "__main__":
    main()