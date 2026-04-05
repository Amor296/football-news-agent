from tavily import TavilyClient
from config import TAVILY_API_KEY, SEARCH_MAX_RESULTS

tavily = TavilyClient(api_key=TAVILY_API_KEY)

def perform_search(query):
    """General tool to search the web and return content."""
    return tavily.search(
        query=query,
        search_depth="advanced",
        max_results=SEARCH_MAX_RESULTS,
        include_raw_content=True,
        search_period="day"
    )