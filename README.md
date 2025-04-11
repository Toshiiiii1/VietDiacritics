# Tự động thêm dấu cho văn bản tiếng Việt không dấu

Ứng dụng mô hình ngôn ngữ lớn trong việc tự động thêm dấu cho văn bản tiếng Việt không dấu

## Quickstart

### Demo với giao diện Streamlit

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

### Chạy demo với giao diện web

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

## Tổng quan
![Sơ đồ tổng quan](images\general.png)

## Thu thập dữ liệu

Nội dung các bài báo thể thao được thu thập từ các trang báo điện tử phổ biến ở Việt Nam qua RSS và bằng cách truy xuất trực tiếp từ trang web với Selenium và Beautiful Soup.

Tổng số bài báo thu thập được: 10,768.

![Thu thập dữ liệu](images\crawl_data.png)

## Tiền xử lý dữ liệu

- Chuẩn hóa Unicode.
- Loại bỏ các ký tự đặc biệt, các đường dẫn.
- Tách câu với thư viện Underthesea.
- Bỏ dấu thanh ở mỗi câu.
- Loại bỏ những câu trùng nhau, những câu quá ngắn (có số lượng từ nhỏ hơn 5).

Các cặp câu không dấu - có dấu được phân chia vào các tập dữ liệu dưới dạng .csv

![Dữ liệu sau tiền xử lý](images\preprocessed_data.png)

|  Set  | Total |
|-----|-------|
| Train set    | 126,234  |
| Val set | 6,556  |
| Test set | 23,081  |