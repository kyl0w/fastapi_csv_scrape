import csv
import requests
from bs4 import BeautifulSoup

def scrape_url(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status() 
        soup = BeautifulSoup(response.content, "html.parser")
        
        title = soup.title.string if soup.title else "No title"
        meta_tags = {meta.get("name"): meta.get("content") for meta in soup.find_all("meta")}
        
        return {"url": url, "title": title, "meta_tags": meta_tags}
    except requests.exceptions.RequestException as e:
        return {"url": url, "error": str(e)}
    
def process_csv(file_content):
    results = []
    csv_reader = csv.reader(file_content)
    for row in csv_reader:
        url = row[0]  
        result = scrape_url(url)
        results.append(result)
    return results
