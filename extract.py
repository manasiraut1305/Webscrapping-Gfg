import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract_article_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Try to get the title from the <h1> tag with class 
        title_tag = soup.find('h1', {'class': 'article-title'})
        if title_tag:
            title = title_tag.get_text()
        else:
            title = 'No title found'
        
        # Try to get the article text from the <div> tag with class 
        article_div = soup.find('div', {'class': 'text'})
        if article_div:
            paragraphs = article_div.find_all('p')
            list_items = article_div.find_all('li')
            strong_tags = article_div.find_all('strong')
        else:
            paragraphs = []
            list_items = []
            strong_tags = []
        
        # Extract text from paragraphs, list items, and strong tags, preserving spaces and structure
        if paragraphs or list_items or strong_tags:
            article_text = '\n\n'.join([p.get_text() for p in paragraphs])
            article_text += '\n\n' + '\n'.join([f"• {li.get_text()}" for li in list_items])
            article_text += '\n\n' + '\n'.join([f"**{strong.get_text()}**" for strong in strong_tags])
        else:
            article_text = 'No article text found'
        
        return title, article_text
    except Exception as e:
        print(f"Error extracting {url}: {e}")
        return 'Error', 'Error'

# Load the input data
df = pd.read_excel('W3input.xlsx')

# Iterate over the URLs and extract text
for index, row in df.iterrows():
    url_id = row['URL_ID']
    url = row['URL']
    print(f"Processing URL ID {url_id}: {url}")
    title, text = extract_article_text(url)
    with open(f'{url_id}.txt', 'w', encoding='utf-8') as f:
        f.write(f"{title}\n\n{text}")

print("Extraction completed.")
