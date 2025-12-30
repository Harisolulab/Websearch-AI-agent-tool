from langchain.agents import tool
 
import requests
import os
 
@tool
def web_search_tool(query: str, count: int = 5) -> dict:
    """
    Perform a real-time web search using the Google Custom Search API.
 
    Args:
        query (str): The user's search query.
        count (int, optional): Number of results to fetch (default: 5).
 
    Returns:
        dict: {
            "status": "success" | "failure",
            "provider": "Google",
            "message": str,
            "results": list[dict]  # Each dict contains title, snippet, url
        }
    """
 
    # ✅ Read API credentials from environment
    api_key = os.getenv("GOOGLE_CSE_API_KEY")
    cx_id = os.getenv("GOOGLE_CSE_ID")
 
    if not api_key or not cx_id:
        return {
            "status": "failure",
            "provider": "Google",
            "message": "Missing Google Custom Search credentials. Set GOOGLE_CSE_API_KEY and GOOGLE_CSE_ID in .env.",
            "results": []
        }
 
    try:
        # 🌐 API endpoint
        url = "https://www.googleapis.com/customsearch/v1"
 
        params = {
            "key": api_key,
            "cx": cx_id,
            "q": query,
            "num": count
        }
 
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
 
        items = data.get("items", [])
        if not items:
            return {
                "status": "success",
                "provider": "Google",
                "message": "No results found.",
                "results": []
            }
 
        # 🧩 Extract structured results
        results = [
            {
                "title": item.get("title", "No title"),
                "snippet": item.get("snippet", "No description available."),
                "url": item.get("link", "")
            }
            for item in items
        ]
 
        return {
            "status": "success",
            "provider": "Google",
            "message": f"Found {len(results)} results for '{query}'.",
            "results": results
        }
 
    except requests.exceptions.RequestException as e:
        return {
            "status": "failure",
            "provider": "Google",
            "message": f"Web search failed: {e}",
            "results": []
        }
