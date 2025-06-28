import requests
import xmltodict
import json
import csv

url = 'http://api.nongsaro.go.kr/service/garden/gardenList'
api_key = '20250626K8HCI4KNPYS4XFEDFUBXVA'

plant_list = []

for page in range(1, 26):
    params = {'apiKey': api_key, 'pageNo': page}
    response = requests.get(url, params=params)
    data_dict = xmltodict.parse(response.content)
    data_json = json.loads(json.dumps(data_dict, ensure_ascii=False))

    items = data_json.get('response', {}).get('body', {}).get('items', {}).get('item', [])
    if isinstance(items, dict):
        items = [items]

    for item in items:
        cntntsNo = item.get('cntntsNo')
        cntntsSj = item.get('cntntsSj')
        if cntntsNo and cntntsSj:
            plant_list.append({'cntntsNo': cntntsNo, 'cntntsSj': cntntsSj})

with open('plant_meta.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['cntntsNo', 'cntntsSj'])
    writer.writeheader()
    writer.writerows(plant_list)
