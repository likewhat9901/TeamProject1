import os
import requests
import xmltodict
import json
import csv
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('WEATHER_API_KEY')

# 초단기실황조회 서비스
url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst'

params ={
  'serviceKey' : api_key,
  'pageNo' : '1',
  'numOfRows' : '100',
  'dataType' : 'XML',
  'base_date' : '20250628',
  'base_time' : '0800',
  'nx' : '60',
  'ny' : '127'
}
response = requests.get(url, params=params)
data_dict = xmltodict.parse(response.content)
data_json = json.loads(json.dumps(data_dict, ensure_ascii=False))

# print(data_json)

# 예보 항목 추출
items = data_json['response']['body']['items']['item']

# 한국어로 컬럼 매핑
column_mapping = {
    'baseDate' : '발표일자',
    'baseTime' : '발표시각',
    'obsrValue' : '실황 값',
    'category' : '자료구분코드',
    'nx' : '예보지점 X 좌표',
    'ny' : '예보지점 Y 좌표'
}

# 카테고리명 한국어로 매핑
category_map = {
    'T1H': '기온',
    'RN1': '1시간 강수량',
    'UUU': '동서바람성분',
    'VVV': '남북바람성분',
    'REH': '습도',
    'PTY': '강수형태',
    'VEC': '풍향',
    'WSD': '풍속'
}
# CSV로 저장
with open('weather_forecast.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    if items:  # 데이터가 있을 경우
        # 첫 행 한국어 키값으로 헤더 지정
        fieldnames = [column_mapping[key] for key in items[0].keys()]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for item in items:
            row = {}
            for key, value in item.items():
                if key == 'category':
                    # 카테고리 코드를 한글로 변경
                    row[column_mapping[key]] = category_map.get(value, value)
                else:
                    # 카테고리 코드가 아니면 값을 그대로
                    row[column_mapping[key]] = value
            writer.writerow(row)