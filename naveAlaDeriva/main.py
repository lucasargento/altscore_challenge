from fastapi import FastAPI, HTTPException, Query
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

@app.get("/phase-change-diagram")
async def reconstruct_phase_diagram(pressure = Query(...)):
    print("Received pressure ", pressure)
    pressure = float(pressure)
    if pressure == 10:
        return {
            "specific_volume_liquid": 0.0035,
            "specific_volume_vapor": 0.0035
            }
    elif pressure == 0.05:
        return {
            "specific_volume_liquid": 0.00105,
            "specific_volume_vapor": 30.00
        }
    else:
        # calculamos las funciones inversas V(p)
        volume_liquid = (pressure + (59/14)) / (199000/49)
        volume_vapor = (pressure - (1199993/119860))/(-(1990/5993))
        return {
            "specific_volume_liquid": volume_liquid,
            "specific_volume_vapor": volume_vapor
        }

@app.post("/teapot")
async def post_teapot():
    """
    Returns an HTTP 418 status code to indicate "I'm a teapot".
    """
    return JSONResponse(status_code=418, content="I'm a teapot")
