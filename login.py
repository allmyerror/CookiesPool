# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     login.py
   Description :   测试登陆
   Author :        SEAN
   date：          2017/12/9
-------------------------------------------------
   Change Activity:
                   2017/12/9:
-------------------------------------------------
"""

import requests
from bs4 import BeautifulSoup

cookies = {
    'SSOLoginState': '1512822152',
    'ALF': '1515414145',
    'SUHB': '0y0oKG9M45s_jO',
    'SUBP': '0033WrSXqPxfM725Ws9jqgMF55529P9D9WheT5D1CoLlW7CZFnJ3VhQG5JpX5K-hUgL.Fozp1KBRe0nNSK52dJLoIpXLxKnL1heLBK2LxKqLBo-LBoMLxKqLBoqL1-iG97tt',
    'SCF': 'AmZK6KcBcYNTB3jr-06slyrQ7nORSizwRBmjDW389cSnXdGh3KxPF--fdVeM-ZUinNXNa-3jPdWY0j1O34CSsK8.',
    'SUB': '_2A253L6XXDeRhGeRP4lYZ8ybLzjyIHXVU08ufrDV6PUJbktBeLULakW1NU-6Yz4hngcKJbvMDlBRU6e0y0D6CnVkE',
    '_T_WM': 'aee085a89aa01842805f274c38e02a52'
}

response = requests.get('https://weibo.cn', cookies=cookies)
if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'lxml')
    title = soup.title.text
    print(title)
