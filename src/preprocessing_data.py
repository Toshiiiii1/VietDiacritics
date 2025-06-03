
import numpy as np
import pandas as pd
from unidecode import unidecode
import re
from sklearn.datasets import load_files
import string
from underthesea import sent_tokenize
import unicodedata

# Chuyển từng câu thành cặp có dấu - không dấu, lưu vào file .csv
def preprocess_text(path):
    # đọc dữ liệu
    df = load_files(f"./{path}", encoding='utf-8')

    """
        - accented_sentences: tập các câu có dấu
        - unaccented_sentences: tập các câu không dấu
    """
    accented_sentences, unaccented_sentences = [], []
    for paragraph in df.data:
        if not "\n" in paragraph:
            # chuẩn hóa unicode
            paragraph = unicodedata.normalize("NFC", paragraph)
            
            # loại bỏ đường dẫn
            paragraph = re.sub(r'http\S+', '', paragraph)
            
            # tách các câu trong bài báo
            sentences = sent_tokenize(paragraph)
            
            # bỏ đi những khoảng trắng thừa
            sentences = [re.sub(r'\s+', " ", sentence) for sentence in sentences]
            
            # chuyển từ câu có dấu -> câu không dấu
            new_sentences = [unidecode(sentence) for sentence in sentences]

            accented_sentences.extend(sentences)
            unaccented_sentences.extend(new_sentences)
    
    # lưu các câu không dấu - có dấu vào data frame
    new_df = pd.DataFrame({'unaccented_sentences': unaccented_sentences, 'accented_sentences': accented_sentences})
    
    # bỏ đi những câu trùng nhau
    new_df.drop_duplicates(inplace=True)
    
    # chọn ra những câu có hơn 5 từ
    new_df['word_count'] = new_df['unaccented_sentences'].apply(lambda x: len(str(x).split()))
    new_df = new_df[(new_df['word_count'] >= 5) & (new_df['word_count'] <= 100)]
    new_df = new_df.drop(columns=["word_count"])
    
    # lưu vào file .csv
    new_df.to_csv(f"{path}.csv", encoding="utf-8", index=False)

if __name__ == "__main__":
    # Tiền xử lý cho tập train, val và test
    preprocess_text("train_set")
    preprocess_text("val_set")
    preprocess_text("test_set")


    train_set = pd.read_csv("./train_set3.csv").astype("str")
    test_set = pd.read_csv("./test_set3.csv").astype("str")
    val_set = pd.read_csv("./val_set3.csv").astype("str")


    # Liệt kê số cặp câu trong mỗi tập và tổng số cặp câu
    print(len(train_set))
    print(len(val_set))
    print(len(test_set))
    print(len(train_set) + len(val_set) + len(test_set))


    # Liệt kê số bài báo của mỗi tập dữ liệu và tổng số bài báo
    train = load_files("./train_set", encoding="utf-8")
    test = load_files("./test_set", encoding="utf-8")
    val = load_files("./val_set", encoding="utf-8")

    print(len(train.data))
    print(len(test.data))
    print(len(val.data))
    print(len(train.data) + len(test.data) + len(val.data))