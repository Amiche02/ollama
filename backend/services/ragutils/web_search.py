from abc import ABC, abstractmethod
from typing import Dict, List

import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS


class WebSearchService(ABC):
    """
    Common interface for a web search + scraping service.
    Subclasses must implement `search_and_scrape(query)`.
    """

    @abstractmethod
    def search_and_scrape(self, query: str) -> List[Dict]:
        """
        Execute a search + retrieve textual content.
        Returns a list of dicts, for example:
            [
              {
                "title": str,
                "url": str,
                "body_snippet": str,
                "raw_text": str
              },
              ...
            ]
        """
        pass


class DuckDuckGoSearchService(WebSearchService):
    """
    A service to perform a DuckDuckGo web search and then scrape results
    *without* using LangChain.
    """

    def __init__(self, max_results: int = 5):
        self.max_results = max_results

    def _search_duckduckgo(self, query: str) -> List[Dict]:
        results = []
        with DDGS() as ddgs:
            for result in ddgs.text(
                query,
                region="wt-wt",
                safesearch="moderate",
                timelimit=None,
                max_results=self.max_results,
            ):
                results.append(result)
        return results

    def _scrape_webpage(self, url: str) -> str:
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Chrome/58.0.3029.110 Safari/537.3"
        }
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            resp.raise_for_status()
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return ""

        soup = BeautifulSoup(resp.content, "lxml")

        # Remove scripts and styles
        for tag in soup(["script", "style", "noscript", "meta", "link"]):
            tag.extract()

        text = soup.get_text(separator="\n").strip()

        # Ensure text is meaningful (avoid empty text)
        if len(text) < 100:  # Can be adjusted
            print(f"⚠️ Skipping {url} (too little text extracted)")
            return ""

        return text

    def search_and_scrape(self, query: str) -> List[Dict]:
        raw_results = self._search_duckduckgo(query)
        output = []
        for item in raw_results:
            url = item.get("href", "")
            if not url:
                continue

            page_text = self._scrape_webpage(url)
            output.append(
                {
                    "title": item.get("title", ""),
                    "url": url,
                    "body_snippet": item.get("body", ""),
                    "raw_text": page_text,
                }
            )
        return output
