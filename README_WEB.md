# Hệ Chuyên Gia Tư Vấn Máy Tính Để Bàn - Phiên Bản Web

Đây là phiên bản web của hệ thống tư vấn máy tính để bàn.

## Yêu cầu

- Python 3.7+
- pip (Python package manager)

## Cài đặt

### 1. Tạo Virtual Environment (Tùy chọn nhưng được khuyên khích)

```bash
# Trên Windows
python -m venv .venv
.venv\Scripts\activate

# Trên macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Cài đặt Dependencies

```bash
pip install -r requirements.txt
```

## Chạy Ứng Dụng

```bash
python app.py
```

Ứng dụng sẽ chạy tại: **http://localhost:5000**

Mở trình duyệt web và truy cập địa chỉ trên.

## Tính năng

✅ **Giao diện Web Responsive** - Hoạt động tốt trên desktop và mobile  
✅ **Hệ thống Tư Vấn Thông Minh** - Gợi ý máy tính phù hợp dựa trên tiêu chí  
✅ **Hiển thị Chi Tiết** - Xem ảnh, mô tả và thông tin đầy đủ về sản phẩm  
✅ **Thông Tin Liên Hệ** - Hiển thị thông tin liên hệ và điều khoản sử dụng  
✅ **API RESTful** - Có sẵn API endpoints để tích hợp với các ứng dụng khác  

## Cấu Trúc Dự Án

```
hechuyengia/
├── app.py                    # Flask application
├── data.py                   # Dữ liệu mapping (thương hiệu, CPU, RAM, etc.)
├── machines_desc.py          # Mô tả chi tiết các máy
├── requirements.txt          # Python dependencies
├── templates/                # HTML templates
│   ├── base.html            # Base template
│   ├── index.html           # Trang chủ
│   └── machine_detail.html  # Trang chi tiết máy
├── static/                   # Static files
│   ├── css/
│   │   └── style.css        # CSS styling
│   ├── js/                  # (Optional) JavaScript files
│   └── images/              # Ảnh máy tính
└── anhmay/                  # Thư mục ảnh gốc (giữ lại cho tham khảo)
```

## API Endpoints

### GET /
Trang chủ - Biểu mẫu tư vấn

### POST /api/recommend
Gửi yêu cầu tư vấn

**Request body:**
```json
{
  "brand": "Dell",
  "purpose": "Văn phòng",
  "special": "Bình thường",
  "cpu": "Core i5",
  "ram": "16GB",
  "ssd": "512GB",
  "price": "15-25 triệu"
}
```

**Response:**
```json
{
  "success": true,
  "p_code": "P5",
  "machine_name": "Dell OptiPlex 7010 Tower",
  "description": "...",
  "image_exists": true,
  "image_url": "/static/images/5.png",
  "selections": {...}
}
```

### GET /api/info
Lấy thông tin liên hệ và điều khoản

### GET /machines/<machine_code>
Xem chi tiết máy tính

## Lưu ý

- Ứng dụng chạy ở chế độ DEBUG. Để production, đặt `debug=False` trong `app.py`
- Các ảnh phải được đặt trong thư mục `static/images/` với tên từ `1.png` đến `24.png`
- Dữ liệu quy tắc được lưu trong `data.py` và không thể thay đổi từ giao diện web (cần chỉnh sửa trực tiếp file)

## Triển Khai (Deployment)

Dự án đã sẵn sàng để deploy lên hosting như Render, PythonAnywhere, Heroku hoặc VPS.

### Cấu hình hỗ trợ deployment
- `Procfile` được thêm để chạy bằng Gunicorn.
- `runtime.txt` xác định Python 3.14.1.
- `requirements.txt` đã bao gồm `gunicorn`.

### Deploy lên Render
1. Tạo tài khoản Render.
2. Tạo dịch vụ Web Service mới.
3. Kết nối repository GitHub/GitLab chứa mã nguồn.
4. Chọn branch và nhấn deploy.
5. Render sẽ tự động cài dependencies và chạy `web: gunicorn app:app`.

### Deploy lên PythonAnywhere
1. Tạo tài khoản PythonAnywhere.
2. Upload mã lên `Files` hoặc kết nối Git.
3. Tạo `Web app` mới, chọn Flask.
4. Chỉnh `WSGI configuration file` để import `app` từ `app.py`.
5. Reload web app.

### Chạy bằng Gunicorn trên server
```bash
pip install -r requirements.txt
gunicorn -w 4 -b 0.0.0.0:$PORT app:app
```

### Lưu ý
- Không dùng Flask development server cho production.
- Mọi người sẽ truy cập được nếu app được deploy trên hosting công khai.
- Nếu cần domain, cấu hình DNS trỏ tới hosting.

## Hỗ Trợ

Email: konamicoco0123@gmail.com  
SĐT: 0329339523  
Địa chỉ: Cao Lãnh, Đồng Tháp, Việt Nam

## Giấy phép

Được tạo năm 2026 - Hệ Chuyên Gia Tư Vấn Máy Tính Để Bàn
