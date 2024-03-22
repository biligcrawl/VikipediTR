import aiohttp
import asyncio
from urllib.parse import quote
from warcio import WARCWriter
from datetime import datetime
from warcio.statusandheaders import StatusAndHeaders
from io import BytesIO
import logging

logging.basicConfig(filename='unexpected_titles.log',
                    level=logging.ERROR,
                    format='%(asctime)s:%(levelname)s:%(message)s')


def log_error(title, error_message):
    logging.error(f"Title: {title}, Error: {error_message}")


async def get_page_titles_and_urls(session, limit=50000):
    url_ = "https://tr.wikipedia.org/w/api.php"
    titles_and_urls = []
    apcontinue = None

    while len(titles_and_urls) < limit:
        params = {
            "action": "query",
            "format": "json",
            "list": "allpages",
            "aplimit": "max",
        }
        if apcontinue:
            params["apcontinue"] = apcontinue

        async with session.get(url=url_, params=params) as response:
            data = await response.json()
            titles_and_urls.extend([
                (page['title'], f"https://tr.wikipedia.org/wiki/{quote(page['title'])}")
                for page in data['query']['allpages']
            ])
            apcontinue = data['continue'].get('apcontinue') if 'continue' in data else None

            if not apcontinue:
                break

    return titles_and_urls[:limit]


async def get_page_content(session, title):
    url_ = "https://tr.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "titles": title,
        "prop": "extracts",
        "explaintext": "true",
    }
    try:
        async with session.get(url=url_, params=params) as response:
            if response.headers["Content-Type"].startswith("application/json"):
                data = await response.json()
                page = next(iter(data['query']['pages'].values()))
                return page.get("extract", "")
            else:
                log_error(title, "Unexpected content type")
                return ""
    except Exception as e:
        log_error(title, str(e))
        return ""


def write_to_warc(data, filename='output.warc'):
    with open(filename, 'wb') as output:
        writer = WARCWriter(output, gzip=True)
        for item in data:
            content, url = item
            http_status = '200 OK'
            headers_list = [('Content-Type', 'text/plain')]
            http_headers = StatusAndHeaders(http_status, headers_list, protocol='HTTP/1.0')
            payload = content.encode('utf-8')
            payload_stream = BytesIO(payload)
            record = writer.create_warc_record(url, 'response', payload=payload_stream, http_headers=http_headers, warc_headers_dict={'WARC-Date': datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')})
            writer.write_record(record)


async def collect_data_and_write_to_warc(limit=5000):
    async with aiohttp.ClientSession() as session:
        titles_and_urls = await get_page_titles_and_urls(session, limit=limit)
        tasks = [get_page_content(session, title) for title, _ in titles_and_urls]
        contents = await asyncio.gather(*tasks)
        data_for_warc = list(zip(contents, [url for _, url in titles_and_urls]))
        write_to_warc(data_for_warc, 'wikipedia_pages.warc')


def main():
    asyncio.run(collect_data_and_write_to_warc(limit=5000))


if __name__ == "__main__":
    main()
