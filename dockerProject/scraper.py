import requests
from bs4 import BeautifulSoup
from kafka import KafkaProducer
import json
import time

# Kafka Producer'ı başlat
producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def scrape_page():
    url = 'https://scrapeme.live/shop/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    products = []

    for product in soup.find_all('li', class_='product'):
        title = product.find('h2', class_='woocommerce-loop-product__title').text
        price = product.find('span', class_='woocommerce-Price-amount amount').text
        products.append({'title': title, 'price': price})

    return products

def main():
    while True:
        data = scrape_page()
        for item in data:
            producer.send('scraped-data', value=item)
            time.sleep(1)  # Her 1 saniyede bir veri gönder
        time.sleep(10)  # Sayfayı her 10 saniyede bir kontrol et

if __name__ == "__main__":
    main()
