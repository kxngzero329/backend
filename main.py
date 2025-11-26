# backend/main.py
from fastapi import FastAPI
from run_spider import run_spider
import json
import os

app = FastAPI()

DATA_FILE = os.path.join(os.path.dirname(__file__), "scraper/data/results.json")

@app.post("/scrape")
def scrape():
    run_spider()
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            results = json.load(f)
        return {"success": True, "results": results}
    return {"success": False, "results": []}
