import os
import re
import sys
import uuid
import pathlib
from datetime import datetime
from urllib.parse import urlparse

load_dotenv('config.env')

class WaymoreParser:
    def __init__(self):
        self._url_ignore_ext_regex = (
            re.compile('\.jpg$|\.jpeg$|\.gif$|\.png$|\.js$|\.zip$|\.pdf$|\.ashx$|\.exe$|\.dmg$|\.txt$|\.xlsx$|\.xls$|'
                       '\.doc$|\.docx$|\.m4v$|\.pptx$|\.ppt$|\.mp4$|\.avi$|\.mp3$', re.IGNORECASE))
        self._urls_result_filename = 'w_p_u_result.txt'
        self._domains_result_filename = 'w_p_d_result.txt'
        self._wayback_max_size = 50000

    def process(self, filepath: str):
        result_domains = os.path.join(os.environ.get("UPLOAD_FOLDER"), self._domains_result_filename)
        result_urls = os.path.join(os.environ.get("UPLOAD_FOLDER"), self._urls_result_filename)
        if os.path.exists(filepath):
            all_urls = []
            domains = set()
            with open(filepath) as infile:
                for url in infile:

                    parsed_parts = urlparse(url)
                    if parsed_parts.netloc not in domains:
                        domains.add(parsed_parts.netloc)

                    all_urls.append(url)

            infile.close()

            urls = self.__filter_urls(all_urls)

            if len(domains) > 0:
                with open(result_domains, "w") as txt_file:
                    for line in domains:
                        txt_file.write(f"{line.strip()}\n")
                txt_file.close()
                print(f'Result - {self._domains_result_filename}')
            else:
                print('No domains results :(')

            if len(urls) > 0:
                with open(result_urls, "w") as txt_file:
                    for line in urls:
                        txt_file.write(f"{line.strip()}\n")
                txt_file.close()
                print(f'Result - {self._urls_result_filename}')
            else:
                print('No urls results :(')

        else:
            print(f'{filepath} not found!')

        return (os.path.join(pathlib.Path().resolve(), result_urls),
                os.path.join(pathlib.Path().resolve(), result_domains))

    def __filter_urls(self, href_urls) -> set:
        urls = set()
        path_without_digits = set()
        added_url_params = {}

        for href_url in href_urls:
            parsed_parts = urlparse(href_url)
            url_without_params = f'{parsed_parts.scheme}://{parsed_parts.netloc}{parsed_parts.path}'
            query_params = {}
            if self._url_ignore_ext_regex.search(parsed_parts.path):
                continue
            if '?' in href_url:
                params = parsed_parts.query.split('&')
                for param in params:
                    split = param.split('=')
                    if len(split) == 2:
                        query_params[split[0]] = split[1]

            if url_without_params in added_url_params:
                added_url_params[url_without_params].update(query_params)
            else:
                added_url_params[url_without_params] = query_params

        for url_without_params in added_url_params:
            params = added_url_params[url_without_params]
            url = url_without_params

            split_path = url_without_params.split('/')
            path_key = ''
            for part in split_path:
                if part.isdigit():
                    path_key += 'numb'
                elif self.__is_valid_hash(part):
                    path_key += 'guid'
                elif self.__is_date(part):
                    path_key += 'date'
                else:
                    path_key += part
            if path_key in path_without_digits:
                continue
            else:
                path_without_digits.add(path_key)

            if len(params) > 0:
                url += '?'

            for key in params:
                url += f'{key}={params[key]}'
            urls.add(url)

        if len(urls) > self._wayback_max_size:
            urls_with_params = set()
            for url_without_params in added_url_params:
                params = added_url_params[url_without_params]
                if len(params) == 0:
                    continue
                url = url_without_params
                for key in params:
                    url += f'{key}={params[key]}'
                urls_with_params.add(url)

            return urls_with_params
        else:
            return urls

    def __is_date(self, string):
        try:
            datetime.strptime(string, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def __is_valid_hash(self, string):

        if re.match(r'^[a-f0-9]{32}$', string):
            return True
        if re.match(r'^[a-f0-9]{16}$', string):
            return True
        try:
            uuid_obj = uuid.UUID(string)
            return str(uuid_obj) == string
        except ValueError:
            return False

if __name__ == '__main__':
    filepath = ''
    if len(sys.argv) == 2:
        filepath = sys.argv[1]
    wp = WaymoreParser()
    result = wp.process(filepath)