import os
import pathlib
import re
from urllib.parse import urlparse
import requests as requests


class SitemapFeed:
    def __init__(self):
        self._headers = {
            'Cache-Control': 'max-age=0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        }
        self._res_filename = os.path.join(os.environ.get("UPLOAD_FOLDER"), 'sitemap_result.txt')

    def process(self, url):
        response = requests.get(url, headers=self._headers)
        regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        urls = re.findall(regex, response.text)
        urls_set = set([x[0] for x in urls if x])

        parsed_parts = urlparse(url)
        main_domain = '.'.join(parsed_parts.netloc.split('.')[-2:])
        with open(self._res_filename, "w") as txt_file:
            for line in urls_set:
                line_domain = urlparse(line)
                if main_domain in line_domain.netloc:
                    txt_file.write(f"{line.strip()}\n")
        txt_file.close()
        print(f'Result - {self._res_filename}')

        return os.path.join(pathlib.Path().resolve(), self._res_filename)
