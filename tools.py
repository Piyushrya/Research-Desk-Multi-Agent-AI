import os
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain.tools import tool
from tavily import TavilyClient

load_dotenv()

_api_key = os.getenv("TAVILY_API_KEY")
tavily = TavilyClient(api_key=_api_key) if _api_key else None


def search_web_direct(query: str, max_results: int = 5) -> list[dict]:
    """Call Tavily directly; avoids spending an LLM call to invoke search."""
    if tavily is None:
        raise RuntimeError("TAVILY_API_KEY is missing. Add it to your .env file.")
    response = tavily.search(query=query, max_results=max_results)
    return response.get("results", [])


def scrape_url_text(url: str, max_chars: int = 3500) -> str:
    """Fetch and clean a public webpage, returning a bounded amount of text."""
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return "Skipped invalid URL."
    if parsed.hostname in {"localhost", "127.0.0.1", "::1"}:
        return "Skipped local URL."

    try:
        response = requests.get(
            url,
            timeout=(3.05, 5),
            headers={"User-Agent": "Mozilla/5.0 (compatible; ResearchDesk/1.0)"},
        )
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header", "noscript", "svg"]):
            tag.decompose()
        text = soup.get_text(separator=" ", strip=True)
        return text[:max_chars] if text else "No readable text found on this page."
    except requests.RequestException as exc:
        return f"Could not scrape URL: {exc}"


@tool
def web_search(query: str) -> str:
    """Search for reliable information and return titles, URLs and snippets."""
    results = search_web_direct(query, max_results=3)
    return "\n\n---\n\n".join(
        f"Title: {item.get('title', 'Untitled')}\n"
        f"URL: {item.get('url', '')}\n"
        f"Snippet: {str(item.get('content', ''))[:300]}"
        for item in results
    ) or "No results found."


@tool
def scrape_url(url: str) -> str:
    """Scrape a public webpage and return clean, relevant text."""
    return scrape_url_text(url, max_chars=3000)
