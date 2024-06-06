import sqlite3
import pandas as pd
from fastapi import HTTPException

def initialize_database_from_txt():
    # 텍스트 파일 경로
    file_path = 'data/extracted_unique_data.txt'
    
    # 텍스트 파일 읽기
    df = pd.read_csv(file_path, delimiter='\t', encoding='utf-8')
    print("TXT data loaded successfully")
    print(df.head())  # 데이터프레임의 첫 몇 줄을 출력하여 확인

    # 데이터프레임의 크기 확인
    print(f"Number of rows in dataframe: {len(df)}")
    
    # SQLite 데이터베이스 연결
    conn = sqlite3.connect('weather_grid.db')
    cur = conn.cursor()

    # 데이터베이스 테이블 생성
    cur.execute('''
    CREATE TABLE IF NOT EXISTS weather_grid (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        단계1 TEXT,
        단계2 TEXT,
        격자_X INTEGER,
        격자_Y INTEGER,
        경도_시 INTEGER,
        경도_분 INTEGER,
        경도_초 REAL,
        위도_시 INTEGER,
        위도_분 INTEGER,
        위도_초 REAL
    )
    ''')
    print("Table created successfully")

    # 데이터프레임의 데이터 삽입
    for index, row in df.iterrows():
        try:
            cur.execute('''
            INSERT INTO weather_grid (단계1, 단계2, 격자_X, 격자_Y, 경도_시, 경도_분, 경도_초, 위도_시, 위도_분, 위도_초)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (row['1단계'], row['2단계'], row['격자 X'], row['격자 Y'], row['경도(시)'], row['경도(분)'], row['경도(초)'], row['위도(시)'], row['위도(분)'], row['위도(초)']))
        except Exception as e:
            print(f"Error inserting row {index}: {e}")
            continue

        # 일정 수의 행마다 커밋
        if index % 100 == 0:
            conn.commit()
            print(f"Committed up to row {index}")

    conn.commit()
    conn.close()
    print("Data inserted successfully")

def search_places(query: str):
    conn = sqlite3.connect('weather_grid.db')
    cur = conn.cursor()
    
    query = f"%{query}%"
    print(f"Searching for places with query: {query}")  # 검색어 출력
    cur.execute('''
    SELECT 단계1, 단계2 FROM weather_grid
    WHERE 단계1 LIKE ? OR 단계2 LIKE ?
    ''', (query, query))
    
    results = cur.fetchall()
    conn.close()
    
    if results:
        places = []
        for result in results:
            place = " ".join([part for part in result if part])
            places.append(place)
        return places
    else:
        return []

def get_grid_coordinates(place_name: str):
    conn = sqlite3.connect('weather_grid.db')
    cur = conn.cursor()
    
    print(f"Searching for coordinates of place: {place_name}")  # 검색어 출력
    cur.execute('''
    SELECT 격자_X, 격자_Y FROM weather_grid
    WHERE 단계1 LIKE ? OR 단계2 LIKE ?
    ''', (f"%{place_name}%", f"%{place_name}%"))
    
    result = cur.fetchone()
    conn.close()
    
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="Location not found")

# 데이터베이스 초기화 함수 실행
initialize_database_from_txt()
