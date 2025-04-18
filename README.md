# Automatically add diacritics to non-diacritic Vietnamese text

Tool to automatically add diacritics to non-diacritic Vietnamese sentences or text. Click [here](./docs/README.md) to see more details.

## Features

- Automatically add diacritics to non-diacritic correctly.
- Has API can be intergrated into other application.
- Support short or long paragraph.

## Quickstart

### Streamlit demo

1. Installation

```bash
# Clone repo
git clone https://github.com/Toshiiiii1/VN_Seq2eq_with_Transformer.git

# Start virtual eviroment
python -m venv venv
source venv/Scripts/activate

# Check venv activate
which python

# Install required Python libraries
pip install -r requirements.txt
```

2. Start demo
```bash
# Navigate to demo folder
cd demo/

# Start Streamlit demo
python -m streamlit run demo.py
```

### Web interface demo

1. Installation

```bash
# Clone repo
git clone https://github.com/Toshiiiii1/VN_Seq2eq_with_Transformer.git

# Start virtual eviroment
python -m venv venv
source venv/Scripts/activate

# Check venv activate
which python

# Install required Python libraries
pip install -r requirements.txt
```

2. Start backend (FastAPI)
```bash
# Navigate to backend folder
cd demo/model_api/

# Start backend, url: http://localhost:8000
uvicorn main:app --port 8000
```

3. Start frontend (ReactJS)
```bash
# Navigate to frontend folder
cd demo/frontend/

# Install required libraries
npm install

# Start frontend
npm run dev
```

### [Video demo](https://drive.google.com/file/d/1zIfLvtkOJKvUmZoSn07qi7UIEOXQkkq6/view?usp=drive_link)

## Technical details

- Large language model: ViT5 Base 1024-length (98.5% accuracy).
- Backend: FastAPI.
- UI: ReactJS, Streamlit.
- Train model: HuggingFace.
- Crawl data: Selenium, Beautiful Soup.
- Preprocess text data: NLTK.

## Acknowledgments
- [VietAI](https://github.com/vietai/ViT5) for the excellent Vietnamese Large language model.
- [FastAPI](https://fastapi.tiangolo.com/) for the excellent framework to build APIs.
- [ReactJS](https://react.dev/) for the amazing framework.