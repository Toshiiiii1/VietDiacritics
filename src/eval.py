from datasets import Dataset
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import numpy as np
import re
import argparse
import torch

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, DataCollatorForSeq2Seq
from tqdm.notebook import tqdm
from torch.utils.data import DataLoader

tokenizer = AutoTokenizer.from_pretrained("VietAI/vit5-base")

def remove_num_and_punc(text):
    result = re.sub(r'[^\w\s]', '', text)
    result = re.sub(r'\b\w*\d+\w*\b', '', result)
    return result

def accuracy(a, b):
    a = remove_num_and_punc(a).split()
    b = remove_num_and_punc(b).split()
    temp = b.copy()
    count = 0

    for i in a:
        if i in temp:
            temp.remove(i)
            count += 1
    if len(a) > len(b):
        return count/len(b)*0.8
    elif len(a) < len(b):
        return count/len(b)*0.6
    else:
        return count/len(b)

def tokenize_texts(texts):
    model_inputs = tokenizer(
        texts["inputs"], max_length=1024, truncation=True
    )

    with tokenizer.as_target_tokenizer():
        labels = tokenizer(
            texts["labels"], max_length=1024, truncation=True
        )
    model_inputs['labels'] = labels['input_ids']
    return model_inputs

def load_and_tokenize_data(data):
    input_lines = data.iloc[:, 0].to_numpy()
    label_lines = data.iloc[:, 1].to_numpy()
    dict_obj = {'inputs': input_lines, 'labels': label_lines}
    dataset = Dataset.from_dict(dict_obj)
    tokenized_dataset = dataset.map(tokenize_texts, batched=True, remove_columns=['inputs'], num_proc=10)

    return tokenized_dataset

def parse_opt():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--weight", type=str, default="", help="Pre-trained model weight")
    parser.add_argument("--test-set", type=str, default="", help="Test data in CSV format")
    
    opt = parser.parse_args()
    
    return opt
    
def eval():
    opt = parse_opt()
    
    test_set = pd.read_csv(opt.test_set).astype("str")
    tokenized_test_set = load_and_tokenize_data(test_set)
    max_target_length = 1024
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    model = AutoModelForSeq2SeqLM.from_pretrained(opt.weight)
    model.to(device)
    
    data_collator = DataCollatorForSeq2Seq(tokenizer, model=model, return_tensors="pt")
    dataloader = DataLoader(tokenized_test_set, collate_fn=data_collator, batch_size=64)

    predictions = []
    references = []
    acc = []

    for i, batch in enumerate(tqdm(dataloader)):
        outputs = model.generate(
            input_ids=batch['input_ids'].to(device),
            max_length=max_target_length,
            attention_mask=batch['attention_mask'].to(device),
        )
        
        with tokenizer.as_target_tokenizer():
            outputs = [tokenizer.decode(out, clean_up_tokenization_spaces=False, skip_special_tokens=True) for out in outputs]

            labels = np.where(batch['labels'] != -100,  batch['labels'], tokenizer.pad_token_id)
            actuals = [tokenizer.decode(out, clean_up_tokenization_spaces=False, skip_special_tokens=True) for out in labels]
            
        predictions.extend(outputs)
        references.extend(actuals)

    for prediction, reference in zip(predictions, references):
        acc.append(accuracy(prediction, reference))
        
    avg_accuracy = np.mean(np.array(acc).astype(np.float32), axis=0)
    
    print(f"Avg accuracy: {avg_accuracy}")

if __name__ == "__main__":
    eval()