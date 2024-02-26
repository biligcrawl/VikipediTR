import csv
import time
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from multiprocessing import Pool, cpu_count


def get_next_page_url(soup):
    next_page_link = soup.select_one('.mw-allpages-nav a[href*="from="]:last-child')
    if next_page_link:
        return 'https://tr.wikipedia.org' + next_page_link['href']
    return None


def get_page_urls(soup):
    page_urls = []
    for link in soup.select('.mw-allpages-body a'):
        url = link.get('href')
        if url and url.startswith('/wiki/'):
            full_url = 'https://tr.wikipedia.org' + url
            page_urls.append(full_url)
    return page_urls


def get_all_page_urls(base_url, pagination_limit=2):
    s = requests.Session()
    all_page_urls = []
    next_page_url = base_url
    pagination_count = 0

    while next_page_url and pagination_count < pagination_limit:
        response = s.get(next_page_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        all_page_urls.extend(get_page_urls(soup))

        next_page_url = get_next_page_url(soup)
        if next_page_url:
            pagination_count += 1

    return all_page_urls


def scrape_page_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = [p.get_text() for p in soup.find_all('p')]
    return ' '.join(paragraphs)


def process_url_chunk(url_chunk):
    results = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_content = {executor.submit(scrape_page_content, url): url for url in url_chunk}
        for future in as_completed(future_to_content):
            content = future.result()
            url = future_to_content[future]
            results.append((content, url))
    return results


def write_to_csv(data, filename='wikipedia.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['content', 'url', 'dtype', 'type', 'length', 'timestamp'])
        for content, url in data:
            writer.writerow([content, url, 'string', 'Wikipedia', len(content.split()), int(time.time())])


def main():
    base_url = 'https://tr.wikipedia.org/wiki/Özel:TümSayfalar'
    pagination_limit = 50
    all_page_urls = get_all_page_urls(base_url, pagination_limit=pagination_limit)

    chunks = [all_page_urls[i::cpu_count()] for i in range(cpu_count())]

    with Pool(cpu_count()) as pool:
        results = pool.map(process_url_chunk, chunks)

    data_for_csv = [item for sublist in results for item in sublist]
    write_to_csv(data_for_csv)


if __name__ == "__main__":
    main()
