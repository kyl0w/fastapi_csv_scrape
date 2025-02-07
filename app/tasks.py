from celery import Celery
from .scrape import scrape_url
import time

celery_app = Celery(
    'scraping_tasks',
    broker='redis://localhost:6379/0', 
    backend='redis://localhost:6379/0'  
)

@celery_app.task(bind=True)
def scrape_urls(self, file_content):
    results = []
    for row in file_content:
        url = row[0] 
        result = scrape_url(url)
        results.append(result)
        time.sleep(1)  
    return results