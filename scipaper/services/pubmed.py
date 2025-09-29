import httpx
from typing import List, Dict, Any
import xml.etree.ElementTree as ET

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

async def search_pubmed(query: str, max_results: int = 10) -> List[str]:
    """Search PubMed for a given query and return a list of article IDs."""
    async with httpx.AsyncClient() as client:
        params = {
            "db": "pubmed",
            "term": query,
            "retmax": max_results,
            "usehistory": "y",
            "retmode": "json"
        }
        response = await client.get(f"{BASE_URL}esearch.fcgi", params=params)
        response.raise_for_status()
        data = response.json()
        return data["esearchresult"]["idlist"]

async def fetch_pubmed_articles(article_ids: List[str]) -> List[Dict[str, Any]]:
    """Fetch the details of a list of PubMed articles by their IDs."""
    async with httpx.AsyncClient() as client:
        params = {
            "db": "pubmed",
            "id": ",".join(article_ids),
            "retmode": "xml"
        }
        response = await client.get(f"{BASE_URL}efetch.fcgi", params=params)
        response.raise_for_status()
        
        root = ET.fromstring(response.content)
        articles = []
        for article in root.findall('.//PubmedArticle'):
            title_element = article.find('.//ArticleTitle')
            title = title_element.text if title_element is not None else "No title found"
            
            pmid_element = article.find('.//PMID')
            pmid = pmid_element.text if pmid_element is not None else ""

            articles.append({
                "source": "pubmed",
                "source_id": pmid,
                "title": title,
            })
        return articles
