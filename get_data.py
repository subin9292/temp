import pandas as pd

def create_unique_txt_from_excel():
    # 엑셀 파일 경로
    file_path = '/mnt/data/기상청41_단기예보 조회서비스_오픈API활용가이드_격자_위경도(20240101).xlsx'
    
    # 엑셀 파일 읽기
    df = pd.read_excel(file_path)
    print("Excel data loaded successfully")
    
    # 필요한 열만 선택
    df_selected = df[['1단계', '2단계', '격자 X', '격자 Y', '경도(시)', '경도(분)', '경도(초)', '위도(시)', '위도(분)', '위도(초)']]

    # 중복 제거 (1단계와 2단계를 기준으로)
    df_unique = df_selected.drop_duplicates(subset=['1단계', '2단계'])

    # 데이터를 텍스트 파일로 저장
    output_file_path = '/mnt/data/extracted_unique_data.txt'
    df_unique.to_csv(output_file_path, sep='\t', index=False, header=True, encoding='utf-8')

    print(f"Data extracted and saved to {output_file_path}")

# 함수 실행
create_unique_txt_from_excel()
