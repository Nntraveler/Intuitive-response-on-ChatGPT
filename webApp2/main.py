import tempfile
from pathlib import Path
import zipfile
import uvicorn
from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.websockets import WebSocket, WebSocketDisconnect
import torch
from pypdf import PdfReader
from pdf2image import convert_from_path
import matplotlib.pyplot as plt
from IPython.display import display
import pdfplumber
import os
import io
from collections import defaultdict
import json
from sentence_transformers import SentenceTransformer, util
import fitz

app = FastAPI()
env = Environment(loader=FileSystemLoader('templates'))

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
app.mount("/data", StaticFiles(directory="data"), name="data")

chat_history = []


class ChatMessage(BaseModel):
    message: str


# use to find the name of the annual report in the corresponding year and the company
def find_pdf_file_in_directory(directory_path):
    files_in_directory = os.listdir(directory_path)

    pdf_files = [file for file in files_in_directory if file.endswith('.pdf')]

    if len(pdf_files) == 1:
        return pdf_files[0]
    elif len(pdf_files) == 0:
        return None
    else:
        return None


def match_page(file_name, prompts, top_k=1):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    reader = PdfReader(file_name)
    corpus = []
    for i, page in enumerate(reader.pages[:]):
        raw_context = page.extract_text()
        context = raw_context.replace('\n', ' ')[:500]
        corpus.append(context)
    corpus_embeddings = model.encode(corpus, convert_to_tensor=True)
    query_embedding = model.encode(prompts, convert_to_tensor=True)
    top_k_indices = util.semantic_search(query_embedding, corpus_embeddings, top_k=top_k)
    return top_k_indices


def covert_pdf_page_to_image(pdf_path, page_numbers, target_directory):
    doc = fitz.open(pdf_path)
    images = []
    for page_number in page_numbers:
        page = doc.load_page(page_number - 1)
        mat = fitz.Matrix(4, 4)
        pix = page.get_pixmap(matrix=mat, dpi=300)
        image_path = os.path.join(target_directory, f"whole_page_{page_number}.png")
        pix.save(image_path)
        images.append(image_path)

    doc.close()
    return images


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
    chat_history = {
        "message": message,
        "year": year,
        "company": company
    }

    print(chat_history["message"])
    # Retrieve the pdf name of the report
    target_directory = f"data/result/{company}_{year}/"
    file_name = os.path.join(target_directory, find_pdf_file_in_directory(target_directory))
    print(file_name)
    top_k = 3
    page_nums = match_page(file_name, chat_history["message"], top_k)[0]
    corpus_ids = [item['corpus_id'] for item in page_nums]
    print(corpus_ids)

    pdf_page_image_urls = covert_pdf_page_to_image(file_name, corpus_ids, target_directory)

    file_list = os.listdir(target_directory)
    result_files = []
    for page_num in corpus_ids:
        page_keyword = f"page_{page_num}_"
        for file in file_list:
            if file.startswith(page_keyword):
                result_files.append(file)
    print(result_files)

    directory = f"data/result/{company}_{year}/"
    print(pdf_page_image_urls)
    images = [directory + image_file for image_file in result_files]

    return templates.TemplateResponse("index.html", {
        "request": request,
        "pdf_pages": json.dumps(pdf_page_image_urls),
        "images": json.dumps(images),
        "filename": file_name
    })


@app.get("/download/{zip_name}")
async def download_zip(zip_name: str):
    zip_path = Path("temp") / zip_name
    if not zip_path.is_file():
        return {"message": "File not found"}
    return FileResponse(path=zip_path, filename=zip_path.name, media_type='application/zip')


@app.post("/back_to_chat")
async def handle_message():
    return RedirectResponse(url='/', status_code=303)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
