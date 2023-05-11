import requests
from bs4 import BeautifulSoup
import json
import re

def scrape():
    
    url = 'https://opinieouczelniach.pl/baza-uczelni/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    
    universities = soup.find_all('a', {'class': 'block text-xl font-medium text-center text-sky-900 uppercase transition-all md:text-left hover:text-sky-800'})
    address_element = soup.find_all('div', 'mx-auto my-4 text-center md:text-left md:ml-0')
    university_list = []

    for university, address in zip(universities, address_element):
        title = university.get('title')
        href = university.get('href')
        address_text = address.get_text().strip()
        city = address_text.split(',')[1].strip()
        match = re.search(r'\d{2}-\d{3}\s+([A-Za-ząćęłńóśźżĄĆĘŁŃÓŚŹŻ ]+)', city)
        if match:
            city2 = match.group(1)
            
        else:
            print('City not found')
        
        university_list.append({
            'title': title,
            'href': 'https://opinieouczelniach.pl' + href,
            'city': city2
        })
         
    with open('universities', 'w', encoding='utf-8') as f:
        json.dump(university_list, f, ensure_ascii=False)
   

if __name__ == '__main__':
    scrape()