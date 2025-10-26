from fastapi import FastAPI
import json
import os

app = FastAPI(docs_url="/api/docs")

with open(os.path.join(os.path.dirname(__file__), 'cs.json')) as f:
    loaded_data = json.load(f)

@app.get("/api/")
async def root():
    return loaded_data