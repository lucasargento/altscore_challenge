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
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Repair Bay</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #2c3e50;
                color: #ecf0f1;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }}
            .container {{
                text-align: center;
                background-color: #34495e;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
            }}
            h1 {{
                font-size: 2.5em;
                margin-bottom: 20px;
            }}
            p {{
                font-size: 1.2em;
            }}
            .system {{
                font-weight: bold;
                color: #e74c3c;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Repair Bay</h1>
            <p>The following system is damaged and needs repair:</p>
            <p class="system">{code}</p>
        </div>
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
