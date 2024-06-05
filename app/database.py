import sqlite3
import pandas as pd
import requests
from fastapi import HTTPException

WEATHER_API_KEY = 'YOUR_SERVICE_KEY'

def initialize_database():
    # 엑셀 파일 경로
    file_path = 'data/기상청41_단기예보 조회서비스_오픈API활용가이드_격자_위경도(20240101).xlsx'
    
    # 엑셀 파일 읽기
    df = pd.read_excel(file_path)
    
    # SQLite 데이터베이스 연결
    conn = sqlite3.connect('weather_grid.db')
    cur = conn.cursor()

    # 데이터베이스 테이블 생성
    cur.execute('''
    CREATE TABLE IF NOT EXISTS weather_grid (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        행정구역코드 TEXT,
        단계1 TEXT,
        단계2 TEXT,
        단계3 TEXT,
        격자_X INTEGER,
        격자_Y INTEGER,
        경도_초_100 REAL,
        위도_초_100 REAL
    )
    ''')
    print("Table created successfully")

    # 데이터프레임의 데이터 삽입
    for index, row in df.iterrows():
        cur.execute('''
        INSERT INTO weather_grid (행정구역코드, 단계1, 단계2, 단계3, 격자_X, 격자_Y, 경도_초_100, 위도_초_100)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (row['행정구역코드'], row['1단계'], row['2단계'], row['3단계'], row['격자 X'], row['격자 Y'], row['경도(초/100)'], row['위도(초/100)']))

    conn.commit()
    conn.close()

def search_places(query: str):
    conn = sqlite3.connect('weather_grid.db')
    cur = conn.cursor()
    
    query = f"%{query}%"
    cur.execute('''
    SELECT 단계1, 단계2, 단계3 FROM weather_grid
    WHERE 단계1 LIKE ? OR 단계2 LIKE ? OR 단계3 LIKE ?
    ''', (query, query, query))
    
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
    
    print(f"Searching for place: {place_name}")
    
    cur.execute('''
    SELECT 격자_X, 격자_Y FROM weather_grid
    WHERE 단계1 LIKE ? OR 단계2 LIKE ? OR 단계3 LIKE ?
    ''', (f"%{place_name}%", f"%{place_name}%", f"%{place_name}%"))
    
    result = cur.fetchone()
    conn.close()
    
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="Location not found")

def get_weather_data(nx: int, ny: int):
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
    params = {
        'serviceKey' : WEATHER_API_KEY,
        'pageNo' : '1', 'numOfRows' : '100', 'dataType' : 'JSON',
        'base_date' : '20240604', 'base_time' : '0500',
        'nx' : nx, 'ny' : ny
    }

    response = requests.get(url, params=params)
    return response.json()
