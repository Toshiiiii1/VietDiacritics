# Tự động thêm dấu cho văn bản tiếng Việt không dấu

Ứng dụng mô hình ngôn ngữ lớn trong việc tự động thêm dấu cho văn bản tiếng Việt không dấu

# Quickstart

## Demo với giao diện Streamlit

1. Install

```bash
# Clone repo
git clone https://github.com/Toshiiiii1/VN_Seq2eq_with_Transformer.git

# Tải các thư viện Python cần thiết
pip install -r requirements.txt
```

2. Chạy demo
```bash
python -m streamlit run demo.py
```

## Chạy demo với giao diện web

1. Install

```bash
# Clone repo
git clone https://github.com/Toshiiiii1/VN_Seq2eq_with_Transformer.git

# Tải các thư viện Python cần thiết
pip install -r requirements.txt
```

2. Chạy backend (FastAPI)
```bash
# Di chuyển đến thư mục backend
cd model_api/

# Chạy backend
uvicorn mainL:app --port 8000
```

3. Chạy frontend (ReactJS)
```bash
# Di chuyển đến thư mục frontend
cd frontend/

# Tải các thư viện cần thiết
npm install

# Chạy frontend
npm run dev
```

# Tổng quan
- Thu thập nội dung các bải báo tiếng Việt về chủ đề thể thao, sau đó tiền xử lý dữ liệu và tạo các cặp câu tiếng Việt không dấu và câu tiếng Việt có dấu cho các tập dữ liệu. Sau đó thực hiện fine-tune mô hình ngôn ngữ ViT5 với tập dữ liệu đã được chuẩn bị để tạo ra mô hình tự động thêm dấu.
