import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime

class FitGirlAPI:
    def __init__(self):
        html_content = requests.get('https://fitgirl-repacks.site').text
        self.soup = BeautifulSoup(html_content,'html.parser')

    def upcoming_release(self):
        entry_div = self.soup.find('div', class_='entry-content')
        title = entry_div.find('h3')
        upcoming = title.find_all('span')
        
        result = []  

        for titles in upcoming:
            title_text = titles.get_text(strip=True).replace('⇢','')
            result.append({"title": title_text})
            
            json_result = {"status": "success",
                        "upcoming_releases": result
                        }
            
        print(json.dumps(json_result, indent=2, ensure_ascii=False))
        return json_result

    def new_release(self):
        
        articles = self.soup.find_all('article', class_=['post', 'type-post'])
        results = []
        today = datetime.today().date()
        
        for article in articles: 
            header = article.find('header', class_='entry-header')
            if not header:
                continue
            
            title_tag = header.find('h1', class_='entry-title')
            if not title_tag:
                continue
            
            title_text = title_tag.get_text(strip=True)
            if 'Upcoming Repacks' in title_text:
                continue
            
            if 'Updates Digest' in title_text:
                continue
            
            a_tag = title_tag.find('a', href=True)
            link = a_tag['href'] if a_tag else None
            
            time_tag = header.find('time', class_='entry-date')
            date = time_tag['datetime'] if time_tag else None
            
            if date:
                try:
                    post_date = datetime.fromisoformat(date).date()
                    if post_date != today:
                        continue
                except ValueError:
                    continue
            else:
                continue
            
            content = article.find('div', class_='entry-content')
            if not content:
                continue
            
            p_tag = content.find('p')
            if not p_tag:
                continue
            
            img = p_tag.find('img')
            image_url = img['src'].strip() if img and img.has_attr('src') else None
            strong = p_tag.find_all('strong')
            company = strong[0].get_text(strip=True) if len(strong) > 0 else None
            languages = strong[1].get_text(strip=True) if len(strong) > 1 else None
            original_size = strong[2].get_text(strip=True) if len(strong) > 2 else None
            repack_size = strong[3].get_text(strip=True) if len(strong) > 3 else None
            
            results.append({
                'title': title_text,
                'link': link,
                'image_url': image_url,
                'company': company,
                'languages': languages,
                'original_size': original_size,
                'repack_size': repack_size,
                'date': date
            })
            
        json_result = {
            'status': 'success',
            'new_releases': results 
        }
        print(json.dumps(json_result, indent=2, ensure_ascii=False))
        return json_result