from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import tensorflow as tf
import numpy as np
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from fastapi.middleware.cors import CORSMiddleware
from underthesea import sent_tokenize

app = FastAPI()

# CORS handle
origins = ["http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class InputText(BaseModel):
    text: str

class OutputText(BaseModel):
    text_with_diacritics: str

# Load your model "A" for adding diacritics
model = AutoModelForSeq2SeqLM.from_pretrained("Toshiiiii1/Vietnamese_diacritics_restoration_5th")
tokenizer = AutoTokenizer.from_pretrained("VietAI/vit5-base")

def add_diacritics(text):
    encoding = tokenizer(text, return_tensors="pt")
    input_ids, attention_masks = encoding["input_ids"], encoding["attention_mask"]
    
    output = model.generate(
        input_ids=input_ids, attention_mask=attention_masks,
        max_length=1024,
    )
        
    result = tokenizer.decode(output[0], skip_special_tokens=True)
    return result

@app.post("/api/add_diacritics/")
def handle_add_diacritics(input_text: InputText):
    text = input_text.text
    result_text = []
    sentences = sent_tokenize(text)
    for sentence in sentences:
        result_text.append(add_diacritics(sentence))

    return {"text_with_diacritics": " ".join(result_text)}
