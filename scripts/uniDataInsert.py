import requests
from bs4 import BeautifulSoup
import json
import mysql.connector


def scrapee():
    
    with open('C:\\path\\to\\universities.json', 'r') as f:
        universities = json.load(f)

    university_urls = []

    for university in universities:
        
        response = requests.get(university['href'])
        soup = BeautifulSoup(response.content, 'html.parser')
        url_element = soup.find('a', {'title': university['title']})
        university_url = url_element['href']
        university_urls.append({
            'title': university['title'],
            'url': university_url,
            'city': university['city']
        })

    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="ProjectIO"
    )


    mycursor = mydb.cursor()
    for university in university_urls:
        sql = "INSERT INTO University (university_name, location, website) VALUES (%s, %s, %s)"
        val = (university['title'], university['city'], university['url'])
        mycursor.execute(sql, val)

    mydb.commit()

if __name__ == '__main__':
    scrapee()
