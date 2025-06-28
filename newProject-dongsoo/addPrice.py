
import pandas as pd

### 식물사전에 가격(price) 추가하기 ###

plants_path = "./resData/plants_kor.csv"
popular_plants_path = "./saveFiles/popular_plants_20250628_1447442.csv"

plants_df = pd.read_csv(plants_path)
popular_df = pd.read_csv(popular_plants_path)

# plants_df에 price 컬럼을 추가하기 위한 준비
# 초기에 NaN(결측치)으로 채워둠
plants_df['가격'] = pd.NA

# popular_df의 각 행을 순회하며 plants_df에 가격 정보 추가
for idx, popular_row in popular_df.iterrows():
    popular_title = popular_row['title']
    popular_price = popular_row['price']

    # plants_df의 '컨텐츠 제목'와 popular_title을 비교
    # '컨텐츠 제목'가 popular_title에 포함되는 경우를 찾음
    # isin 대신 apply와 lambda를 사용하거나, 더 효율적인 문자열 포함 확인 방법 사용
    # 여기서는 간단히 for 루프 안에서 조건 확인
    for p_idx, plant_row in plants_df.iterrows():
        plant_name = plant_row['컨텐츠 제목']
        if pd.notna(plant_name) and plant_name in popular_title:
            # 매칭되면 plants_df에 가격 정보 업데이트
            plants_df.loc[p_idx, '가격'] = popular_price
            # 하나의 popular_title에 여러 식물 이름이 매칭될 수 있으므로,
            # 특정 매칭 기준이 명확하지 않다면 첫 번째 매칭만 반영하거나,
            # 더 정교한 로직이 필요할 수 있습니다.
            break # 첫 번째 매칭되면 다음 popular_title로 넘어감

# 업데이트된 plants_df를 새로운 CSV 파일로 저장
updated_plants_csv_path = "./saveFiles/plants_with_updated_price.csv"
plants_df.to_csv(updated_plants_csv_path, index=False, encoding="utf-8-sig")

print(f"업데이트된 plants_df가 {updated_plants_csv_path}에 저장되었습니다.")