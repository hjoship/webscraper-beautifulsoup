#!/usr/bin/env python3
"""
Simple launcher for the Streamlit Web Scraper App
"""

import subprocess
import sys
import os

def main():
    """Launch the Streamlit application"""
    try:
        # Change to the script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        
        print("🚀 Starting Web Scraper Dashboard...")
        print("📱 The app will open in your default browser")
        print("🛑 Press Ctrl+C to stop the server")
        print("-" * 50)
        
        # Launch Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
        
    except KeyboardInterrupt:
        print("\n👋 Shutting down Web Scraper Dashboard...")
    except Exception as e:
        print(f"❌ Error starting the application: {e}")
        print("Make sure you have installed the dependencies:")
        print("uv run pip install streamlit pandas plotly")

if __name__ == "__main__":
    main()