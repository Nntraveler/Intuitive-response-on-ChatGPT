from sentence_transformers import SentenceTransformer, util
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

def match_page(file_name, prompts, top_k=3):
    reader = PdfReader(file_name)   
    result= dict()
    cos_scores = dict()
    for i, page in enumerate(reader.pages[:]):
        raw_context = page.extract_text()
        result[i] = raw_context
    model = SentenceTransformer('clip-ViT-B-32')
    text_emb = model.encode(prompts)
    for page_i, context in result.items():
        cos_scores[page_i] = util.cos_sim(model.encode([context[:77]]), text_emb)

    top_k_keys = sorted(cos_scores, key=cos_scores.get, reverse=True)[:top_k]
    return top_k_keys


# file_name = "./2022_annual_report_Unilever.pdf"
# prompts = ["Regional growth of ice cream"]
# match_page(file_name, prompts)