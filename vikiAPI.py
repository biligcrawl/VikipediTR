import requests
from urllib.parse import quote
import csv
import time


def get_page_titles_and_urls(limit=20):
    """
    Wikipedia'dan belirtilen limit kadar sayfa başlığını ve URL'lerini çeker.
    """
    s = requests.Session()
    url_ = "https://tr.wikipedia.org/w/api.php"

    params = {
        "action": "query",
        "format": "json",
        "list": "allpages",
        "aplimit": limit
    }

    response = s.get(url=url_, params=params)
    data = response.json()

    titles_and_urls = [(page['title'], f"https://tr.wikipedia.org/wiki/{quote(page['title'])}") for page in
                       data['query']['allpages']]

    return titles_and_urls


def get_page_content(title):
    """
    Verilen başlık için Wikipedia sayfasının içeriğini çeker.
    """
    s = requests.Session()
    url_ = "https://tr.wikipedia.org/w/api.php"

    params = {
        "action": "query",
        "format": "json",
        "titles": title,
        "prop": "extracts",
        "explaintext": True,
    }

    response = s.get(url=url_, params=params)
    data = response.json()
    page = next(iter(data['query']['pages'].values()))
    return page.get("extract", "")


def write_to_csv(data, filename='output.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # CSV başlıkları
        writer.writerow(['content', 'url', 'dtype', 'type', 'length', 'timestamp'])

        for item in data:
            content, url = item
            # Örnek formatınızı takip ederek veri ekleyin
            dtype = 'string'
            type_ = 'book'
            length = len(content.split())  # Kelime sayısını hesapla
            timestamp = int(time.time())  # Unix epoch zamanını al
            writer.writerow([content, url, dtype, type_, length, timestamp])


def collect_data_and_write_to_csv(limit=20):
    titles_and_urls = get_page_titles_and_urls(limit=limit)
    data_for_csv = []

    for title, url in titles_and_urls:
        content = get_page_content(title)
        data_for_csv.append((content, url))

    write_to_csv(data_for_csv, 'wikipedia_api.csv')


def main():
    collect_data_and_write_to_csv(limit=10)


if __name__ == "__main__":
    main()
