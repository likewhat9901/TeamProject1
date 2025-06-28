import csv

input_file = 'weather_forecast.csv'
output_file = 'weather_forecast_kor.csv'

column_mapping = {
    'baseDate' : '발표일자',
    'baseTime' : '발표시각',
    'fcstDate' : '예보일자',
    'fcstTime' : '예보시각',
    'category' : '자료구분문자',
    'fcstValue' : '예보 값',
    'nx' : '예보지점 X 좌표',
    'ny' : '예보지점 Y 좌표'
}


with open(input_file, 'r', encoding='utf-8-sig') as infile, \
     open(output_file, 'w', encoding='utf-8-sig', newline='') as outfile:

    reader = csv.DictReader(infile)
    fieldnames_eng = reader.fieldnames

    # 컬럼명을 한글로 변환 (없는 항목은 그대로 유지)
    fieldnames_kor = [column_mapping.get(col, col) for col in fieldnames_eng]

    writer = csv.DictWriter(outfile, fieldnames=fieldnames_kor)
    writer.writeheader()

    for row in reader:
        writer.writerow({column_mapping.get(k, k): v for k, v in row.items()})
