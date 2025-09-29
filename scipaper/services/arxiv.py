import httpx
from typing import List, Dict, Any
import xml.etree.ElementTree as ET

BASE_URL = "https://export.arxiv.org/api/"

async def search_arxiv(query: str, max_results: int = 10) -> List[Dict[str, Any]]:
    """Search arXiv for a given query and return a list of articles."""
    async with httpx.AsyncClient(follow_redirects=True) as client:
        params = {
            "search_query": query,
            "start": 0,
            "max_results": max_results
        }
        response = await client.get(f"{BASE_URL}query", params=params)
        response.raise_for_status()

        root = ET.fromstring(response.content)
        articles = []
        for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
            title_element = entry.find('{http://www.w3.org/2005/Atom}title')
            title = title_element.text.strip() if title_element is not None else "No title found"

            arxiv_id_element = entry.find('{http://www.w3.org/2005/Atom}id')
            arxiv_id = arxiv_id_element.text.split('/abs/')[-1] if arxiv_id_element is not None else ""

            summary_element = entry.find('{http://www.w3.org/2005/Atom}summary')
            summary = summary_element.text.strip() if summary_element is not None else ""

            authors = [author.find('{http://www.w3.org/2005/Atom}name').text for author in entry.findall('{http://www.w3.org/2005/Atom}author')]

            articles.append({
                "source": "arxiv",
                "source_id": arxiv_id,
                "title": title,
                "abstract": summary,
                "authors": [{"name": author} for author in authors]
            })
        return articles
