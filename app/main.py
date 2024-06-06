from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import pandas as pd

app = FastAPI()

# Static files configuration
app.mount("/static", StaticFiles(directory="static"), name="static")

# 엑셀 파일 경로
file_path = 'data/기상청41_단기예보 조회서비스_오픈API활용가이드_격자_위경도(20240101).xlsx'

# 엑셀 파일 읽기
df = pd.read_excel(file_path)
df_selected = df[['1단계', '2단계', '격자 X', '격자 Y', '경도(시)', '경도(분)', '경도(초)', '위도(시)', '위도(분)', '위도(초)']]
df_unique = df_selected.drop_duplicates(subset=['1단계', '2단계'])

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("static/index.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read(), status_code=200)

@app.get("/search")
def search(query: str):
    query = query.lower()
    results = df_unique[(df_unique['1단계'].str.contains(query, case=False, na=False)) | 
                        (df_unique['2단계'].str.contains(query, case=False, na=False))]
    
    places = results[['1단계', '2단계']].drop_duplicates().apply(lambda row: " ".join(row.dropna()), axis=1).tolist()
    return {"places": places}

@app.get("/coordinates")
def coordinates(place: str):
    # place 문자열을 공백을 기준으로 나누기
    place_parts = place.split()
    
    if len(place_parts) == 1:
        # 1단계만 검색
        results = df_unique[df_unique['1단계'].str.contains(place_parts[0], case=False, na=False)]
    elif len(place_parts) == 2:
        # 1단계와 2단계 모두 검색
        results = df_unique[(df_unique['1단계'].str.contains(place_parts[0], case=False, na=False)) & 
                            (df_unique['2단계'].str.contains(place_parts[1], case=False, na=False))]
    else:
        raise HTTPException(status_code=400, detail="Invalid place format")
    
    if not results.empty:
        result = results.iloc[0]
        nx, ny = result['격자 X'], result['격자 Y']
        print(f"Coordinates for {place}: (X: {nx}, Y: {ny})")
        return {"message": f"Coordinates for {place} are X: {nx}, Y: {ny}"}
    else:
        raise HTTPException(status_code=404, detail="Location not found")
