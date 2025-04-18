import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from unidecode import unidecode

def generate_texts(text):
    model1 = AutoModelForSeq2SeqLM.from_pretrained("./3rd/checkpoint-25500")
    model2 = AutoModelForSeq2SeqLM.from_pretrained("./4th/checkpoint-25500")
    model3 = AutoModelForSeq2SeqLM.from_pretrained("./5th/checkpoint-34000")
    tokenizer = AutoTokenizer.from_pretrained("VietAI/vit5-base")
    
    encoding = tokenizer(text, return_tensors="pt")
    input_ids, attention_masks = encoding["input_ids"], encoding["attention_mask"]
    
    output1 = model1.generate(
        input_ids=input_ids, attention_mask=attention_masks,
        max_length=1024,
    )
    
    output2 = model2.generate(
        input_ids=input_ids, attention_mask=attention_masks,
        max_length=1024,
    )
    output3 = model3.generate(
        input_ids=input_ids, attention_mask=attention_masks,
        max_length=1024,
    )
    
    result1 = tokenizer.decode(output1[0], skip_special_tokens=True)
    result2 = tokenizer.decode(output2[0], skip_special_tokens=True)
    result3 = tokenizer.decode(output3[0], skip_special_tokens=True)
    
    return result1, result2, result3

def main():
    text = st.text_area(label="Text")
    if len(text) > 0:
        accented_text1, accented_text2, accented_text3 = generate_texts(text=text)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.header("Result 1")
            st.write(accented_text1)

        with col2:
            st.header("Result 2")
            st.write(accented_text2)

        with col3:
            st.header("Result 3")
            st.write(accented_text3)

if __name__ == "__main__":
    main()