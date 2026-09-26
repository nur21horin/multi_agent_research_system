from langchain_core.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv
from rich import print
load_dotenv()
tavily=TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query:str)->str:
    """Search the web for recent and reliable information on a topic. Return Titles , URLs and 
    Snippets"""
    response = tavily.search(query=query,max_results=5)
    out=[]
    for i in response['results']:
        out.append(f"Title: {i['title']}\nURL: {i['url']}\nSnippet: {i['content'][:300]}\n")
    return "\n-------\n".join(out)
#print(web_search.invoke("What is the latest news on AI research?"))


@tool 
def scrape_url(url: str) -> str:
    """Scrape and return clean text content from a given URL for deeper reading."""
    try:
        resp = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)[:3000]
    except Exception as e:
        return f"Could not scrape URL: {str(e)}"

#print(scrape_url.invoke("https://www.hindustantimes.com/world-news/russia-sanctions-act-taken-note-of-india-s-warning-that-new-us-tariffs-could-impact-ties-101790363965665.html"))
