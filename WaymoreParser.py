import os
import sys
from urllib.parse import urlparse

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Invalid usage! Example: python WaymoreParser.py waymore/results/target.com/waymore.txt')
    else:
        filepath = sys.argv[1]

        if os.path.exists(filepath):
            urls = []
            domains = set()
            can_add_targets = False
            checked_param_keys = set()
            with open(filepath) as infile:
                for url in infile:

                    parsed_parts = urlparse(url)
                    if parsed_parts.netloc not in domains:
                        domains.add(parsed_parts.netloc)

                    if '?' not in url:
                        continue
                    else:
                        params = parsed_parts.query.split('&')
                        param_names = set()
                        for param in params:
                            param_names.add(param.split('=')[0])
                        curr_key = ";".join(list(param_names))
                        if curr_key not in checked_param_keys:
                            checked_param_keys.add(curr_key)
                            urls.append(url)

            infile.close()

            if len(domains) > 0:
                with open('w_p_d_result.txt', "w") as txt_file:
                    for line in urls:
                        txt_file.write(f"{line.strip()}\n")
                txt_file.close()
                print('Result - w_p_d_result.txt')
            else:
                print('No domains results :(')

            if len(urls) > 0:
                with open('w_p_u_result.txt', "w") as txt_file:
                    for line in urls:
                        txt_file.write(f"{line.strip()}\n")
                txt_file.close()
                print('Result - w_p_u_result.txt')
            else:
                print('No urls results :(')

        else:
            print(f'{filepath} not found!')
