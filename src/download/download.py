import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import os


def download_s3_directories(bucket_url, prefix, local_dir):

    response = requests.get(bucket_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'xml')
        keys = soup.find_all('Key')

        for key in keys:
            file_name = key.text
            if file_name.startswith(prefix):
                file_url = urljoin(bucket_url, file_name)
                local_file_path = os.path.join(local_dir, file_name.split('/')[-1])

                file_response = requests.get(file_url)
                if file_response.status_code == 200:
                    with open(local_file_path, 'wb') as f:
                        f.write(file_response.content)
                    print(f"{file_name} downloaded.")
                else:
                    print(f"{file_name} could not be downloaded: HTTP {file_response.status_code}")
    else:
        print(f"Failed to access the bucket: HTTP {response.status_code}")

bucket_url = 'https://biligcrawlopenturkishdata.s3.amazonaws.com'
prefix = 'WikipediaTR'
local_dir = 'data'

if not os.path.exists(local_dir):
    os.makedirs(local_dir)

download_s3_directories(bucket_url, prefix, local_dir)
