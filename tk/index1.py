import requests
from bs4 import BeautifulSoup
import pandas as pd

def search_tiktok(keyword):
    url = f"https://www.tiktok.com/search?q={keyword}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve data: {response.status_code}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

def parse_tiktok_data(soup):
    with open('test.txt','w') as f:
        f.write(soup.text())
    exit()
    data = []
    for user in soup.find_all('div', class_='user-info'):
        name = user.find('h2', class_='user-name').text.strip()
        bio = user.find('p', class_='user-bio').text.strip()
        followers = user.find('span', class_='follower-count').text.strip()
        data.append({'Name': name, 'Bio': bio, 'Followers': followers})

    return pd.DataFrame(data)

def main():
    keyword = "your_keyword_here"
    soup = search_tiktok(keyword)
    if soup:
        tiktok_data = parse_tiktok_data(soup)
        print(tiktok_data)
    else:
        print("No data found")

if __name__ == "__main__":
    main()
