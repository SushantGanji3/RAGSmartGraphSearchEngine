"""Data ingestion from Wikipedia API."""
import wikipedia
import json
import os
from typing import List, Dict
from bs4 import BeautifulSoup
import re

class WikipediaScraper:
    """Scrape and clean Wikipedia articles."""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        wikipedia.set_lang("en")
    
    def clean_text(self, text: str) -> str:
        """Remove HTML, extra whitespace, and clean text."""
        soup = BeautifulSoup(text, "html.parser")
        text = soup.get_text()
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?;:\-\'"]', '', text)
        return text.strip()
    
    def extract_links(self, page) -> List[str]:
        """Extract related Wikipedia links from page."""
        try:
            links = page.links[:10]  # Top 10 related links
            return links
        except:
            return []
    
    def scrape_topic(self, topic: str, max_pages: int = 50) -> List[Dict]:
        """Scrape Wikipedia articles on a given topic."""
        documents = []
        
        try:
            # Search for the topic
            search_results = wikipedia.search(topic, results=max_pages)
            
            for i, title in enumerate(search_results[:max_pages]):
                try:
                    page = wikipedia.page(title, auto_suggest=False)
                    
                    # Clean content
                    content = self.clean_text(page.content)
                    summary = self.clean_text(page.summary)
                    
                    # Extract related entities
                    related_entities = self.extract_links(page)
                    
                    doc = {
                        "id": i + 1,
                        "title": page.title,
                        "content": content[:5000],  # Limit content length
                        "summary": summary,
                        "source_link": page.url,
                        "related_entities": related_entities
                    }
                    
                    documents.append(doc)
                    print(f"Scraped: {page.title}")
                    
                except wikipedia.exceptions.DisambiguationError as e:
                    # Handle disambiguation pages
                    try:
                        page = wikipedia.page(e.options[0], auto_suggest=False)
                        content = self.clean_text(page.content)
                        summary = self.clean_text(page.summary)
                        related_entities = self.extract_links(page)
                        
                        doc = {
                            "id": i + 1,
                            "title": page.title,
                            "content": content[:5000],
                            "summary": summary,
                            "source_link": page.url,
                            "related_entities": related_entities
                        }
                        documents.append(doc)
                        print(f"Scraped (disambiguation): {page.title}")
                    except:
                        continue
                        
                except Exception as e:
                    print(f"Error scraping {title}: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error in search: {e}")
        
        # Save to JSON
        output_file = os.path.join(self.data_dir, f"{topic.replace(' ', '_')}_data.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(documents, f, indent=2, ensure_ascii=False)
        
        print(f"\nScraped {len(documents)} documents. Saved to {output_file}")
        return documents

