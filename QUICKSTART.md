# 🚀 Hướng Dẫn Chạy Nhanh (Quick Start)

## Yêu cầu

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) đã cài và đang chạy
- [Git](https://git-scm.com/downloads)

---

## Cách 1: Docker Compose (Khuyến nghị)

```bash
# 1. Clone project
git clone <repository-url>
cd english-learning-app

# 2. Build và khởi động tất cả services
docker-compose up --build
```

Đợi khoảng **5–10 phút** (lần đầu build). Khi thấy log backend chạy xong migration và seed data là sẵn sàng.

### Truy cập ứng dụng

| Dịch vụ | URL |
|---------|-----|
| 🌐 Frontend | http://localhost |
| 🔌 Backend API | http://localhost:8081 |
| 📚 Swagger Docs | http://localhost:8081/swagger/ |
| 🔧 Admin Panel | http://localhost:8081/admin/ |

### Các lệnh hữu ích

```bash
# Chạy ngầm (background)
docker-compose up -d

# Xem logs realtime
docker-compose logs -f

# Dừng tất cả services
docker-compose down

# Xóa toàn bộ (kể cả database) — CẨN THẬN!
docker-compose down -v
```

---

## Cách 2: Chạy thủ công (không dùng Docker)

Yêu cầu thêm: Python 3.11+, Node.js 18+, PostgreSQL 15+, Redis 7+

### Backend

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py seed_db
python manage.py runserver
```

### Frontend (terminal khác)

```bash
cd frontend
npm install --legacy-peer-deps
npm start
```

Frontend chạy tại `http://localhost:3000`.

---

## Dữ liệu mẫu có sẵn

Sau khi chạy, hệ thống đã được seed sẵn:

- 📖 **50 từ vựng** phổ biến (kèm phiên âm, ví dụ)
- 📚 **3 khóa học** (Beginner / Business / Advanced) — mỗi khóa 5 bài học
- 🎮 **3 bài quiz** tương ứng

> Cần tạo tài khoản admin? Chạy: `docker-compose exec backend python manage.py createsuperuser`

---

## Troubleshooting nhanh

| Vấn đề | Giải pháp |
|--------|-----------|
| Docker không kết nối | Mở Docker Desktop, đợi biểu tượng cá voi chuyển xanh |
| Port 80 đã dùng | Đổi port trong `docker-compose.yml`: `"3000:80"` |
| Database lỗi | `docker-compose restart postgres` → `docker-compose restart backend` |
| Build thất bại | `docker system prune -a` rồi build lại |

Xem hướng dẫn đầy đủ tại [docs/guide/user-guide.md](docs/guide/user-guide.md).
