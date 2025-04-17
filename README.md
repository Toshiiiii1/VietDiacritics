# Tự động thêm dấu cho văn bản tiếng Việt không dấu

Công cụ giúp tự động thêm dấu câu cho câu hoặc văn bản tiếng Việt không dấu.

## Tính năng chính

- Thêm dấu câu chính xác cho văn bản tiếng Việt.
- API sẵn sàng tích hợp vào các ứng dụng khác.
- Hỗ trợ cả văn bản dài và ngắn.

## Sử dụng

### Demo với giao diện Streamlit

1. Cài đặt

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

### Chạy demo với giao diện web

1. Cài đặt

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

# Chạy backend, url: http://localhost:8000
uvicorn main:app --port 8000
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

### [Video demo](https://drive.google.com/file/d/1zIfLvtkOJKvUmZoSn07qi7UIEOXQkkq6/view?usp=drive_link)

## Công nghệ sử dụng

- Mô hình ngôn ngữ: ViT5 phiên bản Base 1024-length (98.5% độ chính xác).
- Backend: FastAPI.
- UI: ReactJS, Streamlit (demo nhanh)