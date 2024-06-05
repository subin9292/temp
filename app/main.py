from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.database import search_places, get_grid_coordinates

app = FastAPI()

# Static files configuration
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("static/index.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read(), status_code=200)

@app.get("/search")
def search(query: str):
    places = search_places(query)
    return {"places": places}

@app.get("/coordinates")
def coordinates(place: str):
    nx, ny = get_grid_coordinates(place)
    print(f"Coordinates for {place}: (X: {nx}, Y: {ny})")
    return {"message": f"Coordinates for {place} printed to console."}
