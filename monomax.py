import requests
import json
import re
from bs4 import BeautifulSoup

response = requests.get(url='https://monomax.by/map')
soup = BeautifulSoup(response.text, 'html.parser')
addresses = soup.find_all('p', attrs={'class': 'name'})
phones = soup.find_all('p', attrs={'class': 'phone'})
addresses_text = [a.text for a in addresses]
phones_text = [p.text for p in phones if p.text]

script = soup.find_all('script', attrs={'type': 'text/javascript'})[-1].text
pattern = re.compile(r'\d{2}[.]\d{3,}')
coordinates = re.findall(r'\[.*\]', script)[1:]

res = []
with open('monomax.json', 'w', encoding='utf8') as f:
    for i in range(0, len(addresses_text)):
        one = {
            'address': addresses_text[i],
            'latlon': coordinates[i],
            'name': 'Мономах',
            'phones': phones_text[i]
        }
        res.append(one)
    json.dump(obj=res, fp=f, ensure_ascii=False, indent=4)
