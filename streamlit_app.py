#!/usr/bin/env python3
"""
Streamlit Web Scraper Application
Interactive web scraping tool with data visualization
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import re
from urllib.parse import urlparse
import time
from datetime import datetime

# Import our web scraper classes
from webscraper import WebScraper, NewsScraper, EcommerceScraper, save_to_csv, save_to_json

# Configure Streamlit page
st.set_page_config(
    page_title="Web Scraper Dashboard",
    page_icon="🕷️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #c3e6cb;
    }
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #f5c6cb;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'scraped_data' not in st.session_state:
        st.session_state.scraped_data = []
    if 'scraping_history' not in st.session_state:
        st.session_state.scraping_history = []
    if 'current_scraper' not in st.session_state:
        st.session_state.current_scraper = None

def validate_url(url):
    """Validate if the URL is properly formatted"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def detect_website_type(url):
    """Detect the type of website for appropriate scraping strategy"""
    url_lower = url.lower()
    
    if any(news_indicator in url_lower for news_indicator in ['news', 'cnn', 'bbc', 'reuters', 'guardian']):
        return 'news'
    elif any(shop_indicator in url_lower for shop_indicator in ['shop', 'store', 'amazon', 'ebay', 'etsy']):
        return 'ecommerce'
    else:
        return 'general'

def scrape_general_content(url):
    """Scrape general content from any website"""
    scraper = WebScraper()
    soup = scraper.get_page(url)
    
    if not soup:
        return None
    
    # Extract various elements
    data = {
        'url': url,
        'title': soup.title.string if soup.title else 'No title',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
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
    
    # Extract images
    images = scraper.extract_images(soup, url)
    
    # Extract paragraphs
    paragraphs = []
    for p in soup.find_all('p'):
        text = p.get_text(strip=True)
        if len(text) > 20:  # Filter out short paragraphs
            paragraphs.append({
                'text': text,
                'length': len(text),
                'word_count': len(text.split())
            })
    
    return {
        'metadata': data,
        'headings': headings,
        'links': links[:50],  # Limit to first 50 links
        'images': images[:20],  # Limit to first 20 images
        'paragraphs': paragraphs[:30]  # Limit to first 30 paragraphs
    }

def scrape_quotes_site(url):
    """Specialized scraper for quotes websites"""
    scraper = WebScraper()
    soup = scraper.get_page(url)
    
    if not soup:
        return None
    
    quotes = []
    
    # Try different quote selectors
    quote_selectors = [
        {'container': 'div.quote', 'text': 'span.text', 'author': 'small.author'},
        {'container': '.quote', 'text': '.text', 'author': '.author'},
        {'container': 'blockquote', 'text': 'p', 'author': 'cite'}
    ]
    
    for selectors in quote_selectors:
        quote_elements = soup.select(selectors['container'])
        if quote_elements:
            for quote in quote_elements:
                text_elem = quote.select_one(selectors['text'])
                author_elem = quote.select_one(selectors['author'])
                
                if text_elem:
                    quote_text = text_elem.get_text(strip=True)
                    author = author_elem.get_text(strip=True) if author_elem else 'Unknown'
                    
                    quotes.append({
                        'text': quote_text,
                        'author': author,
                        'length': len(quote_text),
                        'word_count': len(quote_text.split())
                    })
            break
    
    return {
        'metadata': {
            'url': url,
            'title': soup.title.string if soup.title else 'Quotes',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_quotes': len(quotes)
        },
        'quotes': quotes
    }

def create_data_visualizations(data, data_type):
    """Create various visualizations based on scraped data"""
    
    if data_type == 'general':
        # Create tabs for different visualizations
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📝 Headings", "🔗 Links", "📷 Images"])
        
        with tab1:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Headings", len(data['headings']))
            with col2:
                st.metric("Total Links", len(data['links']))
            with col3:
                st.metric("Total Images", len(data['images']))
            with col4:
                st.metric("Total Paragraphs", len(data['paragraphs']))
            
            # Content distribution pie chart
            if data['headings'] or data['links'] or data['images'] or data['paragraphs']:
                fig = px.pie(
                    values=[len(data['headings']), len(data['links']), len(data['images']), len(data['paragraphs'])],
                    names=['Headings', 'Links', 'Images', 'Paragraphs'],
                    title="Content Distribution"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            if data['headings']:
                # Headings analysis
                headings_df = pd.DataFrame(data['headings'])
                
                # Heading levels distribution
                fig1 = px.histogram(headings_df, x='level', title="Heading Levels Distribution")
                st.plotly_chart(fig1, use_container_width=True)
                
                # Heading lengths
                fig2 = px.scatter(headings_df, x='level', y='length', 
                                title="Heading Length by Level", hover_data=['text'])
                st.plotly_chart(fig2, use_container_width=True)
                
                # Show headings table
                st.subheader("All Headings")
                st.dataframe(headings_df, use_container_width=True)
            else:
                st.info("No headings found on this page.")
        
        with tab3:
            if data['links']:
                st.subheader(f"Found {len(data['links'])} Links")
                
                # Categorize links
                internal_links = [link for link in data['links'] if urlparse(data['metadata']['url']).netloc in link]
                external_links = [link for link in data['links'] if urlparse(data['metadata']['url']).netloc not in link]
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Internal Links", len(internal_links))
                with col2:
                    st.metric("External Links", len(external_links))
                
                # Links pie chart
                if internal_links or external_links:
                    fig = px.pie(
                        values=[len(internal_links), len(external_links)],
                        names=['Internal', 'External'],
                        title="Link Types Distribution"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                # Show links
                links_df = pd.DataFrame({'URL': data['links']})
                st.dataframe(links_df, use_container_width=True)
            else:
                st.info("No links found on this page.")
        
        with tab4:
            if data['images']:
                st.subheader(f"Found {len(data['images'])} Images")
                
                # Show images in a grid
                cols = st.columns(3)
                for i, img in enumerate(data['images'][:9]):  # Show first 9 images
                    with cols[i % 3]:
                        try:
                            st.image(img['src'], caption=img['alt'][:50] if img['alt'] else 'No caption', width=200)
                        except:
                            st.text(f"Image: {img['src'][:50]}...")
                
                # Images table
                images_df = pd.DataFrame(data['images'])
                st.dataframe(images_df, use_container_width=True)
            else:
                st.info("No images found on this page.")
    
    elif data_type == 'quotes':
        if data['quotes']:
            quotes_df = pd.DataFrame(data['quotes'])
            
            # Overview metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Quotes", len(quotes_df))
            with col2:
                st.metric("Unique Authors", quotes_df['author'].nunique())
            with col3:
                st.metric("Avg Quote Length", f"{quotes_df['length'].mean():.0f} chars")
            with col4:
                st.metric("Avg Word Count", f"{quotes_df['word_count'].mean():.0f} words")
            
            # Visualizations
            tab1, tab2, tab3 = st.tabs(["📊 Analytics", "👥 Authors", "📝 Quotes"])
            
            with tab1:
                # Quote length distribution
                fig1 = px.histogram(quotes_df, x='length', title="Quote Length Distribution")
                st.plotly_chart(fig1, use_container_width=True)
                
                # Word count vs character count
                fig2 = px.scatter(quotes_df, x='word_count', y='length', 
                                title="Word Count vs Character Count", hover_data=['author'])
                st.plotly_chart(fig2, use_container_width=True)
            
            with tab2:
                # Authors analysis
                author_counts = quotes_df['author'].value_counts().head(10)
                fig3 = px.bar(x=author_counts.index, y=author_counts.values, 
                            title="Top 10 Authors by Quote Count")
                st.plotly_chart(fig3, use_container_width=True)
                
                # Author stats
                st.subheader("Author Statistics")
                st.dataframe(quotes_df.groupby('author').agg({
                    'length': ['count', 'mean'],
                    'word_count': 'mean'
                }).round(2), use_container_width=True)
            
            with tab3:
                # Show all quotes
                st.subheader("All Quotes")
                for i, quote in quotes_df.iterrows():
                    with st.expander(f"Quote {i+1} by {quote['author']}"):
                        st.write(f"*\"{quote['text']}\"*")
                        st.caption(f"Length: {quote['length']} characters, {quote['word_count']} words")
        else:
            st.info("No quotes found on this page.")

def main():
    """Main Streamlit application"""
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">🕷️ Web Scraper Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 Scraping Configuration")
        
        # URL input
        url = st.text_input("Enter URL to scrape:", placeholder="https://example.com")
        
        # Scraping options
        st.subheader("Scraping Options")
        scraper_type = st.selectbox(
            "Scraper Type:",
            ["Auto-detect", "General Content", "Quotes Site", "News Site", "E-commerce"]
        )
        
        # Advanced options
        with st.expander("Advanced Options"):
            delay_min = st.slider("Min delay (seconds)", 0.5, 5.0, 1.0, 0.5)
            delay_max = st.slider("Max delay (seconds)", 1.0, 10.0, 3.0, 0.5)
            timeout = st.slider("Request timeout (seconds)", 5, 30, 10)
            max_items = st.slider("Max items to scrape", 10, 100, 50)
        
        # Scrape button
        scrape_button = st.button("🚀 Start Scraping", type="primary", use_container_width=True)
        
        # History
        if st.session_state.scraping_history:
            st.subheader("📜 Scraping History")
            for i, item in enumerate(reversed(st.session_state.scraping_history[-5:])):
                if st.button(f"🔄 {item['url'][:30]}...", key=f"history_{i}"):
                    url = item['url']
                    scrape_button = True
    
    # Main content area
    if scrape_button and url:
        if not validate_url(url):
            st.error("❌ Please enter a valid URL (including http:// or https://)")
            return
        
        # Show scraping progress
        with st.spinner("🕷️ Scraping website..."):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Determine scraping strategy
                if scraper_type == "Auto-detect":
                    detected_type = detect_website_type(url)
                    status_text.text(f"Detected website type: {detected_type}")
                elif scraper_type == "General Content":
                    detected_type = "general"
                elif scraper_type == "Quotes Site":
                    detected_type = "quotes"
                else:
                    detected_type = "general"
                
                progress_bar.progress(25)
                
                # Scrape based on type
                if detected_type == "quotes" or "quotes" in url.lower():
                    status_text.text("Scraping quotes...")
                    scraped_data = scrape_quotes_site(url)
                    data_type = "quotes"
                else:
                    status_text.text("Scraping general content...")
                    scraped_data = scrape_general_content(url)
                    data_type = "general"
                
                progress_bar.progress(75)
                
                if scraped_data:
                    # Store in session state
                    st.session_state.scraped_data = scraped_data
                    st.session_state.scraping_history.append({
                        'url': url,
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'type': data_type
                    })
                    
                    progress_bar.progress(100)
                    status_text.text("✅ Scraping completed successfully!")
                    
                    # Success message
                    st.success(f"🎉 Successfully scraped data from {url}")
                    
                    # Display results
                    st.markdown("## 📊 Scraped Data Analysis")
                    create_data_visualizations(scraped_data, data_type)
                    
                    # Download options
                    st.markdown("## 💾 Download Data")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if data_type == "quotes" and scraped_data.get('quotes'):
                            csv_data = pd.DataFrame(scraped_data['quotes']).to_csv(index=False)
                            st.download_button(
                                "📄 Download as CSV",
                                csv_data,
                                f"scraped_quotes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                "text/csv"
                            )
                        elif data_type == "general":
                            # Create a summary CSV
                            summary_data = {
                                'metric': ['Headings', 'Links', 'Images', 'Paragraphs'],
                                'count': [
                                    len(scraped_data.get('headings', [])),
                                    len(scraped_data.get('links', [])),
                                    len(scraped_data.get('images', [])),
                                    len(scraped_data.get('paragraphs', []))
                                ]
                            }
                            csv_data = pd.DataFrame(summary_data).to_csv(index=False)
                            st.download_button(
                                "📄 Download Summary CSV",
                                csv_data,
                                f"scraped_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                "text/csv"
                            )
                    
                    with col2:
                        json_data = json.dumps(scraped_data, indent=2, default=str)
                        st.download_button(
                            "📋 Download as JSON",
                            json_data,
                            f"scraped_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                            "application/json"
                        )
                
                else:
                    st.error("❌ Failed to scrape data from the website. Please check the URL and try again.")
                
            except Exception as e:
                st.error(f"❌ An error occurred while scraping: {str(e)}")
            
            finally:
                progress_bar.empty()
                status_text.empty()
    
    # Show example URLs
    if not st.session_state.scraped_data:
        st.markdown("## 🌟 Try These Example URLs")
        
        example_urls = [
            {"name": "Quotes to Scrape", "url": "http://quotes.toscrape.com/", "type": "Quotes"},
            {"name": "Wikipedia", "url": "https://en.wikipedia.org/wiki/Web_scraping", "type": "General"},
            {"name": "Hacker News", "url": "https://news.ycombinator.com/", "type": "News"},
            {"name": "GitHub Trending", "url": "https://github.com/trending", "type": "General"}
        ]
        
        cols = st.columns(2)
        for i, example in enumerate(example_urls):
            with cols[i % 2]:
                if st.button(f"🔗 {example['name']}", key=f"example_{i}"):
                    st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "Built with ❤️ using Streamlit and Beautiful Soup | "
        "[GitHub Repository](https://github.com/hjoship/webscraper-beautifulsoup)"
    )

if __name__ == "__main__":
    main()