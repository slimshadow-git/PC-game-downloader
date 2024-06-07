import streamlit as st
import requests
from bs4 import BeautifulSoup

def search_game_results(game_name):
    search_url = f"https://gamingbeasts.com/?s={game_name}"
    response = requests.get(search_url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        game_entries = soup.find_all('div', class_='inside-article')
        
        if not game_entries:
            return None
        
        results = []
        for entry in game_entries:
            title_elem = entry.find('h2', class_='entry-title').find('a')
            title = title_elem.text if title_elem else "Title not found"
            link = title_elem['href'] if title_elem else "Link not found"
            
            categories_elem = entry.find('span', class_='cat-links')
            categories = [category.text for category in categories_elem.find_all('a')] if categories_elem else []
            
            results.append({
                'title': title,
                'link': link,
                'categories': categories
            })
        
        return results
    else:
        return None

def scrape_download_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        url_input_elem = soup.find('input', {'name': 'url'})
        
        if url_input_elem:
            download_url = url_input_elem['value']
            return download_url
    return None

def get_download_urls(game_name):
    results = search_game_results(game_name)
    
    if isinstance(results, list):
        download_urls = []
        for result in results:
            download_url = scrape_download_url(result['link'])
            if download_url:
                download_urls.append(download_url)
        
        return download_urls
    else:
        return None

st.title("Game Download URL Finder")

game_name = st.text_input("Enter the name of the game:")
if game_name:
    download_urls = get_download_urls(game_name)
    
    if download_urls:
        st.subheader(f"Download URLs for '{game_name}':")
        for i, download_url in enumerate(download_urls, start=1):
            st.write(f"{i}. {download_url}")
    else:
        st.write("No download URLs found for this game.")
