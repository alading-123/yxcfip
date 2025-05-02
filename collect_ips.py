import requests
from bs4 import BeautifulSoup
import re
import os

# 目标 URL 列表
urls = [
    'https://monitor.gacjie.cn/page/cloudflare/ipv4.html', 
    'https://ip.164746.xyz'
]

# IP 正则表达式
ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'

# 存储唯一 IP 的集合
ip_set = set()

for url in urls:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 根据网站结构查找元素
        elements = soup.find_all('tr')  # 两个网址都用 <tr>
        
        for element in elements:
            text = element.get_text()
            matches = re.findall(ip_pattern, text)
            ip_set.update(matches)
    
    except Exception as e:
        print(f'抓取 {url} 时出错: {e}')

# 写入去重后的 IP 到文件
with open('ip.txt', 'w') as f:
    for ip in sorted(ip_set):
        f.write(ip + '\n')

print(f'共保存 {len(ip_set)} 个唯一 IP 到 ip.txt。')
