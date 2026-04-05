import os
from dotenv import load_dotenv
from tavily import TavilyClient
from tools.search_tools import perform_search
# Load environment variables
load_dotenv()

# Initialize Tavily client
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def get_football_news(query):
    """
    Search for detailed football news focusing on names and specific details.
    Uses include_raw_content to get more text for the AI to analyze.
    """
    # Refining the query to force the search engine to find names and clubs
    full_query = f"confirmed football transfer news {query} players names 2026 details"
    print(f"🔎 Deep searching for specific details about: {query}...")
    
    # Execute search with higher limits and raw content
    search_result = tavily.search(
        query=full_query, 
        search_depth="advanced", 
        max_results=7,             # Increased to 7 for better data coverage
        include_raw_content=True,  # Pulls more text from the website pages
        search_period="day"        # Last 24 hours only
    )
    return search_result