import os
import pathlib
import re
from urllib.parse import urlparse
import requests as requests
from dotenv import load_dotenv


class SwaggerLinkFinder:
    def __init__(self):
        self._headers = {
            'Cache-Control': 'max-age=0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        }
        self._res_filename = os.path.join(os.environ.get("UPLOAD_FOLDER"), 'swagger_result.txt')

    def process(self, url):
        response = requests.get(url, headers=self._headers)
        if response.status_code != 200:
            print(f'Exit flow. StatusCode: {response.status_code}')
            return
        parsed_parts = urlparse(url)
        basic_url = f'{parsed_parts.scheme}://{parsed_parts.netloc}'
        result = set()
        lines = response.text.split('\n')
        for i in range(len(lines)):
            line = lines[i]
            if '"/' in line:
                path = line.split('"')[1]
                if i + 1 < len(lines):
                    next_line = lines[i+1]
                    method = None
                    if '"get"' in next_line:
                        method = 'get'
                    elif '"post"' in next_line:
                        method = 'get'
                    elif '"patch"' in next_line:
                        method = 'patch'
                    elif '"delete"' in next_line:
                        method = 'delete'
                    elif '"put"' in next_line:
                        method = 'put'

                    if not method:
                        continue
                    result.add(f'{basic_url}{path}')

        with open(self._res_filename, "w") as txt_file:
            for line in result:
                txt_file.write(f"{line.strip()}\n")
        txt_file.close()
        print(f'Result - {self._res_filename}')

        return os.path.join(pathlib.Path().resolve(), self._res_filename)


if __name__ == '__main__':
    load_dotenv('config.env')
    url = 'https://prod-eu1-asana-cell01-6551918b.asana.argocd.app.asana.com/swagger.json'
    wp = SwaggerLinkFinder()
    result = wp.process(url)
