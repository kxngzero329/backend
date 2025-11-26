from fastapi import FastAPI
from run_spider import run_pnp_spider
import json

app = FastAPI()

@app.get("/scrape/pnp")
def scrape_pnp():
    try:
        run_pnp_spider()
        with open("scraper/data/results.json") as f:
            data = json.load(f)
        return {"success": True, "results": data}
    except Exception as e:
        return {"success": False, "error": str(e)}
