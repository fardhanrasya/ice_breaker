# from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()


def get_profile_url_tavily(name: str):
    """searches for the linkedin page"""
    client = TavilyClient("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")
    res = client.search(query=name)
    return res
