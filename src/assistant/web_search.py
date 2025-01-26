from typing import List, Dict
from tavily import TavilyClient
from .configuration import Configuration

def web_search(query: str, config: Configuration) -> List[Dict]:
    """Basic web search using Tavily API"""
    try:
        tavily = TavilyClient(api_key=config.tavily_api_key)
        response = tavily.search(
            query=query,
            search_depth="basic",
            max_results=5,
            include_answer=True
        )
        return response.get('results', [])
    
    except Exception as e:
        print(f"Search error: {e}")
        return []

def tavily_search(query: str, config: Configuration) -> List[Dict]:
    """Advanced search with RAG-optimized context"""
    try:
        tavily = TavilyClient(api_key=config.tavily_api_key)
        context = tavily.get_search_context(
            query=query,
            search_depth="advanced",
            max_results=7,
            include_answer=True,
            include_images=True
        )
        return [{
            "content": context,
            "sources": tavily.get_search_results(query, 7)
        }]
    
    except Exception as e:
        print(f"Tavily search error: {e}")
        return [] 