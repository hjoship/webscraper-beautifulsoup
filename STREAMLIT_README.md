# 🕷️ Web Scraper Dashboard - Streamlit App

An interactive web application for scraping websites and visualizing data using Beautiful Soup and Streamlit.

## 🚀 Quick Start

### Option 1: Using the Launcher Script
```bash
uv run python run_app.py
```

### Option 2: Direct Streamlit Command
```bash
uv run streamlit run streamlit_app.py
```

The app will automatically open in your browser at `http://localhost:8501`

## ✨ Features

### 🎯 **Interactive Web Scraping**
- Enter any URL and scrape data instantly
- Auto-detection of website types (quotes, news, general content)
- Real-time progress tracking with status updates
- Error handling with user-friendly messages

### 📊 **Data Visualization**
- **Overview Dashboard**: Key metrics and content distribution
- **Interactive Charts**: Plotly-powered visualizations
- **Data Tables**: Sortable and filterable data views
- **Content Analysis**: Word counts, lengths, and patterns

### 🎨 **Specialized Scrapers**
- **Quotes Sites**: Extract quotes with authors and tags
- **General Content**: Headlines, links, images, and paragraphs
- **News Sites**: Article extraction (configurable)
- **E-commerce**: Product information (configurable)

### 💾 **Data Export**
- Download scraped data as CSV or JSON
- Automatic timestamping of exports
- Summary reports for general content

### 🔧 **Advanced Configuration**
- Adjustable request delays (1-10 seconds)
- Timeout settings (5-30 seconds)
- Maximum items limit (10-100)
- Custom headers support

## 📱 User Interface

### Sidebar Controls
- **URL Input**: Enter the website to scrape
- **Scraper Type**: Auto-detect or manual selection
- **Advanced Options**: Delays, timeouts, limits
- **Scraping History**: Quick access to previous URLs

### Main Dashboard
- **Progress Tracking**: Real-time scraping status
- **Tabbed Visualizations**: Organized data views
- **Interactive Charts**: Hover for details
- **Download Buttons**: Export data instantly

## 🎯 Example Use Cases

### 1. **Quotes Analysis**
```
URL: http://quotes.toscrape.com/
- Extracts quotes with authors and tags
- Analyzes quote lengths and word counts
- Shows author statistics and distributions
- Interactive quote browser
```

### 2. **Content Research**
```
URL: https://en.wikipedia.org/wiki/Web_scraping
- Extracts all headings (H1-H6)
- Collects internal and external links
- Gathers images with alt text
- Analyzes paragraph content
```

### 3. **News Monitoring**
```
URL: https://news.ycombinator.com/
- Extracts headlines and articles
- Categorizes internal vs external links
- Content distribution analysis
- Export for further processing
```

## 📊 Visualization Types

### **Overview Charts**
- Pie charts for content distribution
- Metrics cards for quick stats
- Progress bars for scraping status

### **Content Analysis**
- Histogram of text lengths
- Scatter plots for correlations
- Bar charts for top categories
- Word cloud visualizations (planned)

### **Interactive Tables**
- Sortable data columns
- Expandable content rows
- Search and filter capabilities
- Export selected data

## 🛠️ Technical Details

### **Architecture**
```
streamlit_app.py
├── Session State Management
├── URL Validation & Detection
├── Scraping Functions
│   ├── scrape_general_content()
│   ├── scrape_quotes_site()
│   └── scrape_news_headlines()
├── Visualization Functions
│   ├── create_data_visualizations()
│   └── Interactive Plotly Charts
└── Data Export Functions
```

### **Data Flow**
```
User Input → URL Validation → Website Detection → 
Scraping → Data Processing → Visualization → Export
```

### **Error Handling**
- Network timeout protection
- Invalid URL detection
- Missing element graceful handling
- User-friendly error messages

## 🎨 Customization

### **Themes**
The app uses a custom color scheme:
- Primary: `#1f77b4` (Blue)
- Background: `#ffffff` (White)
- Secondary: `#f0f2f6` (Light Gray)

### **Adding New Scrapers**
1. Create a new scraping function
2. Add to the scraper type dropdown
3. Implement visualization logic
4. Update the detection algorithm

### **Custom Visualizations**
```python
# Add to create_data_visualizations()
fig = px.scatter(data, x='metric1', y='metric2')
st.plotly_chart(fig, use_container_width=True)
```

## 🔍 Troubleshooting

### **Common Issues**

1. **App won't start**
   ```bash
   # Check dependencies
   uv run pip list | grep streamlit
   
   # Reinstall if needed
   uv add streamlit pandas plotly
   ```

2. **Scraping fails**
   - Check internet connection
   - Verify URL is accessible
   - Try increasing timeout settings
   - Check if site blocks scrapers

3. **Visualizations not showing**
   - Ensure data was scraped successfully
   - Check browser console for errors
   - Try refreshing the page

### **Performance Tips**
- Use smaller delay ranges for faster scraping
- Limit max items for large sites
- Close unused browser tabs
- Use headless mode for better performance

## 🚀 Deployment Options

### **Local Development**
```bash
uv run streamlit run streamlit_app.py --server.port 8501
```

### **Streamlit Cloud** (Recommended)
1. Push code to GitHub
2. Connect to Streamlit Cloud
3. Deploy with one click
4. Share public URL

### **Docker Deployment**
```dockerfile
FROM python:3.11-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py"]
```

## 📈 Future Enhancements

- [ ] **Scheduled Scraping**: Set up recurring scrapes
- [ ] **Data Persistence**: Save scraping history to database
- [ ] **Advanced Filters**: More sophisticated data filtering
- [ ] **Bulk URLs**: Scrape multiple URLs at once
- [ ] **API Integration**: Connect to external APIs
- [ ] **Machine Learning**: Content classification and analysis
- [ ] **Real-time Updates**: Live data streaming
- [ ] **User Authentication**: Personal dashboards

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your enhancements
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

---

**Built with ❤️ using Streamlit, Beautiful Soup, and Plotly**