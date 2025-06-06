from datasets import Dataset
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import torch
import numpy as np
import re

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, DataCollatorForSeq2Seq, Seq2SeqTrainer,Seq2SeqTrainingArguments
from tqdm.notebook import tqdm
from torch.utils.data import DataLoader
from datasets import load_metric

tokenizer = AutoTokenizer.from_pretrained("VietAI/vit5-base")
model = AutoModelForSeq2SeqLM.from_pretrained("VietAI/vit5-base")
model.to('cuda')

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

def train(train_csv, val_csv):
    train_set = pd.read_csv(train_csv).astype("str")
    val_set = pd.read_csv(val_csv).astype("str")
    
    tokenized_train_set = load_and_tokenize_data(train_set)
    tokenized_val_set = load_and_tokenize_data(val_set)
    
    data_collator = DataCollatorForSeq2Seq(tokenizer, model=model, return_tensors="pt")

    training_args = Seq2SeqTrainingArguments(
        output_dir="/kaggle/working/3th",
        do_train=True,
        do_eval=True,
        num_train_epochs=3,
        learning_rate=1e-5,
        warmup_ratio=0.05,
        weight_decay=0.01,
        per_device_train_batch_size=9,
        per_device_eval_batch_size=4,
        logging_dir='/kaggle/working/3th',
        group_by_length=True,
        save_strategy="steps",
        save_steps=500,
        save_total_limit=1,
        evaluation_strategy="steps",
        eval_steps=500,
        fp16=True,
    )

    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_train_set,
        data_collator=data_collator,
        eval_dataset=tokenized_val_set
    )
    
    trainer.train()
    
def eval(model, test_csv):
    test_set = pd.read_csv(test_csv).astype("str")
    tokenized_test_set = load_and_tokenize_data(test_set)
    max_target_length = 1024
    data_collator = DataCollatorForSeq2Seq(tokenizer, model=model, return_tensors="pt")
    dataloader = DataLoader(tokenized_test_set, collate_fn=data_collator, batch_size=64)

    predictions = []
    references = []
    acc = []

    for i, batch in enumerate(tqdm(dataloader)):
        outputs = model.generate(
            input_ids=batch['input_ids'].to('cuda'),
            max_length=max_target_length,
            attention_mask=batch['attention_mask'].to('cuda'),
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
    
    return avg_accuracy

if __name__ == "__main__":
    train_csv = "/kaggle/input/temp-data/train_set.csv"
    val_csv = "/kaggle/input/temp-data/val_set.csv"
    test_csv = "/kaggle/input/temp-data/test_set.csv"
    
    train(train_csv, val_csv)
    model = AutoModelForSeq2SeqLM.from_pretrained("/kaggle/input/vit5-model-3thh")
    model.to('cuda')
    eval(test_csv)