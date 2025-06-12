from datasets import Dataset
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import argparse

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, DataCollatorForSeq2Seq, Seq2SeqTrainer,Seq2SeqTrainingArguments

tokenizer = AutoTokenizer.from_pretrained("VietAI/vit5-base")

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
    parser.add_argument("--train-set", type=str, default="", help="Train data in VOC format")
    parser.add_argument("--val-set", type=str, default="", help="Validation data in VOC format")
    parser.add_argument("--output-path", type=str, default="", help="Validation data in VOC format")
    
    opt = parser.parse_args()
    
    return opt

def train():
    opt = parse_opt()
    
    train_set = pd.read_csv(opt.train_set).astype("str")
    val_set = pd.read_csv(opt.val_set).astype("str")
    
    model = AutoModelForSeq2SeqLM.from_pretrained(opt.weight)
    model.to("cuda")
    
    tokenized_train_set = load_and_tokenize_data(train_set)
    tokenized_val_set = load_and_tokenize_data(val_set)
    
    data_collator = DataCollatorForSeq2Seq(tokenizer, model=model, return_tensors="pt")

    training_args = Seq2SeqTrainingArguments(
        output_dir=opt.output_path,
        do_train=True,
        do_eval=True,
        num_train_epochs=1,
        learning_rate=1e-5,
        warmup_ratio=0.05,
        weight_decay=0.01,
        per_device_train_batch_size=9,
        per_device_eval_batch_size=4,
        logging_dir=opt.output_path,
        logging_strategy="no",
        group_by_length=True,
        save_strategy="steps",
        save_steps=500,
        save_total_limit=1,
        eval_strategy="steps",
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

if __name__ == "__main__":
    train()