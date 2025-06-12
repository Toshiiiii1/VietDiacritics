from datasets import Dataset
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import numpy as np
import re
import argparse
import torch
import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, DataCollatorForSeq2Seq
from tqdm.notebook import tqdm
from torch.utils.data import DataLoader

def parse_opt():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--weight", type=str, default="", help="Pre-trained model weight")
    parser.add_argument("--sentence", type=str, default="", help="non-diacritic sentence")
    
    opt = parser.parse_args()
    
    return opt

def main():
    opt = parse_opt()
    
    tokenizer = AutoTokenizer.from_pretrained("VietAI/vit5-base")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    model = AutoModelForSeq2SeqLM.from_pretrained(opt.weight)
    model.to(device)
    
    encoding = tokenizer(opt.sentence, return_tensors="pt")
    input_ids, attention_masks = encoding["input_ids"], encoding["attention_mask"]
    
    output = model.generate(
        input_ids=input_ids, attention_mask=attention_masks,
        max_length=1024,
    )
    
    for output in output:
        line = tokenizer.decode(output, skip_special_tokens=True)
        print(f"Diacritics sentence: {line}", end="\n\n")

if __name__ == '__main__':
    main()