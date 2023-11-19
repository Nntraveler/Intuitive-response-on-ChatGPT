from pathlib import Path

import uvicorn
from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.websockets import WebSocket, WebSocketDisconnect

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup Jinja2 templates for FastAPI
template_folder = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=template_folder)
app.mount("/static", StaticFiles(directory="static"), name="static")
chat_history = []
class ChatMessage(BaseModel):
    message: str

@app.get("/styles.css", response_class=FileResponse)
def styles():
    return FileResponse('static/css/styles.css')

@app.get("/")
async def read_index():
    print(template_folder)
    return FileResponse('index.html')

@app.post("/start_new_chat")
async def start_new_chat():
    # Redirect to the home page
    return RedirectResponse(url='/', status_code=303)

@app.post("/send_message")
async def handle_message(
    request: Request,
    message: str = Form(...),
    year: str = Form(...),
    company: str = Form(...)
):
    chat_history.append({
        "message": message,
        "year": year,
        "company": company
    })

    return FileResponse('result.html')
if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)