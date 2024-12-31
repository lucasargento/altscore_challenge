from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse,JSONResponse
import random

# run using uvicorn main:app --host 0.0.0.0 --port 8000
app = FastAPI()

# System to code mapping
SYSTEM_CODE_MAPPING = {
    "navigation": "NAV-01",
    "communications": "COM-02",
    "life_support": "LIFE-03",
    "engines": "ENG-04",
    "deflector_shield": "SHLD-05"
}

# Randomly select a damaged system
damaged_system = random.choice(list(SYSTEM_CODE_MAPPING.keys()))

@app.get("/status")
async def get_status():
    """
    Returns the damaged system as a JSON response.
    """
    
    return {"damaged_system": damaged_system}

@app.get("/repair-bay", response_class=HTMLResponse)
async def get_repair_bay():
    """
    Returns an HTML page with the corresponding system code.
    """
    code = SYSTEM_CODE_MAPPING.get(damaged_system, "UNKNOWN")
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Repair</title>
    </head>
    <body>
    <div class="anchor-point">{code}</div>
    </body>
    </html>    
    """
    return HTMLResponse(content=html_content, status_code=200)


@app.post("/teapot")
async def post_teapot():
    """
    Returns an HTTP 418 status code to indicate "I'm a teapot".
    """
    return JSONResponse(status_code=418, content="I'm a teapot")
