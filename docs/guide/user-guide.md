# 📘 Hướng Dẫn Sử Dụng English Learning Platform

> **Tác giả**: ToànLD  
> **Phiên bản**: 1.0.0  
> **Ngày cập nhật**: 26/05/2026  
> **Ngôn ngữ**: Tiếng Việt

---

## 📑 Mục Lục

1. [Giới thiệu](#-giới-thiệu)
2. [Yêu cầu hệ thống](#-yêu-cầu-hệ-thống)
3. [Cài đặt](#-cài-đặt)
4. [Khởi chạy](#-khởi-chạy)
5. [Hướng dẫn sử dụng](#-hướng-dẫn-sử-dụng)
   - [Đăng ký tài khoản](#1-đăng-ký-tài-khoản)
   - [Đăng nhập](#2-đăng-nhập)
   - [Dashboard](#3-dashboard)
   - [Danh sách khóa học](#4-danh-sách-khóa-học)
   - [Chi tiết khóa học](#5-chi-tiết-khóa-học)
   - [Xem bài học](#6-xem-bài-học)
   - [Flashcard từ vựng](#7-flashcard-từ-vựng)
   - [Làm bài Quiz](#8-làm-bài-quiz)
   - [Trang cá nhân](#9-trang-cá-nhân)
6. [Quản trị viên](#-quản-trị-viên)
7. [API Reference](#-api-reference)
8. [Troubleshooting](#-troubleshooting)
9. [FAQ](#-faq)

---

## 🎯 Giới thiệu

**English Learning Platform** là một nền tảng học tiếng Anh trực tuyến hoàn chỉnh với các tính năng:

- 📚 **Khóa học**: Học theo bài học có cấu trúc (3 khóa học, 15 bài học)
- 📝 **Từ vựng**: 50 từ vựng phổ biến với flashcard và phát âm
- 🎮 **Quiz**: Kiểm tra kiến thức với trắc nghiệm và điền từ
- 📊 **Thống kê**: Theo dõi tiến độ học tập với biểu đồ
- 🔊 **Phát âm**: Nghe phát âm từ vựng bằng Web Speech API
- 🏆 **Gamification**: Hệ thống XP, streak, level

### 🏗️ Kiến trúc hệ thống

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Frontend  │ ◄──► │   Backend   │ ◄──► │  PostgreSQL │
│ (React + TS)│      │ (Django DRF)│      │  Database   │
└─────────────┘      └─────────────┘      └─────────────┘
                            │
                            ▼
                     ┌─────────────┐
                     │    Redis    │
                     │  (Celery)   │
                     └─────────────┘
```

### Công nghệ sử dụng

| Layer | Công nghệ |
|-------|-----------|
| Frontend | React 18, TypeScript, Redux Toolkit, TailwindCSS, Recharts |
| Backend | Django 5, Django REST Framework, JWT Auth |
| Database | PostgreSQL 16 |
| Cache/Queue | Redis 7, Celery |
| Infrastructure | Docker, Nginx, Gunicorn |

---

## 💻 Yêu cầu hệ thống

### Phần mềm bắt buộc

| Phần mềm | Phiên bản tối thiểu | Link tải |
|----------|---------------------|----------|
| **Docker Desktop** | 4.x+ | [Tải tại đây](https://www.docker.com/products/docker-desktop/) |
| **Git** | 2.x+ | [Tải tại đây](https://git-scm.com/downloads) |

### Cấu hình máy tối thiểu

- **RAM**: 4 GB (khuyến nghị 8 GB)
- **Dung lượng ổ cứng**: 5 GB trống
- **CPU**: 2 nhân trở lên
- **Hệ điều hành**: Windows 10/11, macOS 10.15+, Linux

### Cổng mạng cần mở

| Cổng | Dịch vụ |
|------|---------|
| `80` | Frontend (Nginx) |
| `8000` | Backend API (Django) |
| `5432` | PostgreSQL (chỉ internal) |
| `6379` | Redis (chỉ internal) |

---

## ⚙️ Cài đặt

### Bước 1: Cài đặt Docker Desktop

**Windows:**
1. Tải Docker Desktop từ trang chủ
2. Chạy file cài đặt `Docker Desktop Installer.exe`
3. Khởi động lại máy khi được yêu cầu
4. Mở Docker Desktop và đợi biểu tượng cá voi chuyển sang **xanh lá** (Running)

**macOS:**
```bash
# Tải bằng Homebrew
brew install --cask docker
# Mở Docker từ Applications
```

**Linux (Ubuntu/Debian):**
```bash
# Cài đặt Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Cài đặt Docker Compose
sudo apt install docker-compose-plugin
newgrp docker
```

### Bước 2: Kiểm tra Docker đã sẵn sàng

```bash
docker --version
# Output: Docker version 24.x.x, build xxxxx

docker compose version
# Output: Docker Compose version v2.x.x
```

### Bước 3: Clone project

```bash
git clone https://github.com/your-username/english-learning-app.git
cd english-learning-app
```

### Bước 4: Cấu hình môi trường

Copy file `.env.example` thành `.env`:

```bash
# Windows PowerShell
Copy-Item .env.example .env

# Linux/macOS
cp .env.example .env
```

**Các biến môi trường quan trọng:**

| Biến | Mô tả | Giá trị mặc định |
|------|-------|------------------|
| `SECRET_KEY` | Khóa bí mật Django | (tự động sinh) |
| `DATABASE_URL` | Kết nối PostgreSQL | `postgres://postgres:postgres@postgres:5432/english_platform` |
| `REDIS_URL` | Kết nối Redis | `redis://redis:6379/0` |
| `DJANGO_ALLOWED_HOSTS` | Host được phép | `localhost,127.0.0.1,backend` |
| `CORS_ALLOWED_ORIGINS` | Nguồn CORS | `http://localhost` |

---

## 🚀 Khởi chạy

### Khởi động lần đầu

```bash
docker-compose up --build
```

Lệnh này sẽ:
1. ✅ Build image cho backend (Django) và frontend (React)
2. ✅ Khởi động PostgreSQL, Redis
3. ✅ Chạy migrations tự động
4. ✅ Load dữ liệu mẫu (50 từ vựng, 3 khóa học, 15 bài học, quizzes)
5. ✅ Khởi động Celery worker và beat

**Thời gian build lần đầu**: ~5-10 phút

### Sau lần đầu

```bash
# Khởi động (không build lại)
docker-compose up

# Chạy ngầm (background)
docker-compose up -d

# Xem logs realtime
docker-compose logs -f

# Xem logs của 1 service cụ thể
docker-compose logs -f backend
docker-compose logs -f frontend

# Dừng tất cả
docker-compose down

# Xóa toàn bộ (cả database) — CẨN THẬN!
docker-compose down -v
```

### Truy cập các dịch vụ

| Dịch vụ | URL | Mô tả |
|---------|-----|-------|
| 🌐 **Frontend** | http://localhost | Giao diện người dùng |
| 🔌 **Backend API** | http://localhost:8000 | API root |
| 📚 **Swagger Docs** | http://localhost:8000/swagger/ | Tài liệu API interactive |
| 📖 **ReDoc** | http://localhost:8000/redoc/ | API docs dạng đọc |
| 🔧 **Admin Panel** | http://localhost:8000/admin/ | Quản trị hệ thống |

### Kiểm tra dịch vụ

```bash
# Xem trạng thái các container
docker-compose ps

# Kiểm tra sức khỏe
curl http://localhost:8000/health/
# Response: {"status": "ok"}
```

---

## 📖 Hướng dẫn sử dụng

### 1. Đăng ký tài khoản

**URL**: `http://localhost/register`

**Các bước:**

1. Truy cập trang **Đăng ký**
2. Điền thông tin:
   - **Username**: Tên đăng nhập (chữ thường, số, không dấu cách)
   - **Email**: Địa chỉ email hợp lệ
   - **Password**: Mật khẩu (tối thiểu 8 ký tự)
   - **Confirm Password**: Nhập lại mật khẩu
   - **Full Name**: Họ và tên (tùy chọn)
3. Nhấn nút **Đăng ký**
4. Hệ thống tự động đăng nhập và chuyển đến Dashboard

**Quy tắc mật khẩu:**
- Tối thiểu 8 ký tự
- Nên bao gồm chữ hoa, chữ thường, số, ký tự đặc biệt
- Không được quá đơn giản (như `123456`, `password`)

---

### 2. Đăng nhập

**URL**: `http://localhost/login`

**Các bước:**

1. Truy cập trang **Đăng nhập**
2. Nhập **Username** và **Password**
3. Nhấn nút **Đăng nhập**
4. Chuyển đến Dashboard sau khi đăng nhập thành công

**Lưu ý:**
- JWT access token có hiệu lực **1 ngày**
- Refresh token có hiệu lực **7 ngày**
- Tự động refresh token khi access token hết hạn
- Nếu refresh token hết hạn → cần đăng nhập lại

---

### 3. Dashboard

**URL**: `http://localhost/dashboard`

Dashboard là trang chính sau khi đăng nhập, hiển thị tổng quan quá trình học tập.

#### 📊 Các chỉ số thống kê

| Chỉ số | Mô tả | Cách tăng |
|--------|-------|-----------|
| **Total XP** | Tổng điểm kinh nghiệm | Học bài, làm quiz |
| **Current Level** | Cấp độ hiện tại | Tích lũy đủ XP |
| **Current Streak** | Chuỗi ngày học liên tiếp | Học ít nhất 1 bài/ngày |
| **Words Learned** | Số từ vựng đã học | Ôn flashcard |
| **Quizzes Completed** | Số bài quiz đã hoàn thành | Làm quiz |
| **Courses Enrolled** | Số khóa học đã đăng ký | Đăng ký khóa học |

#### 📈 Biểu đồ hoạt động

- **Biểu đồ đường (Line Chart)**: XP tích lũy theo 7 ngày gần nhất
- **Biểu đồ cột (Bar Chart)**: Hoạt động học tập theo ngày
- **Biểu đồ tròn (Pie Chart)**: Phân bổ thời gian theo loại hoạt động

#### 🎯 Mục tiêu hàng ngày

- Hoàn thành ít nhất 1 bài học
- Học 10 từ vựng mới
- Làm 1 bài quiz

**Bảng XP:**

| Hoạt động | XP nhận được |
|-----------|-------------|
| Hoàn thành 1 bài học | +20 XP |
| Học 1 từ vựng mới | +5 XP |
| Hoàn thành quiz | +50 XP |
| Quiz đạt 100% | +100 XP bonus |
| Duy trì streak | +10 XP/ngày |

---

### 4. Danh sách khóa học

**URL**: `http://localhost/courses`

Hiển thị tất cả khóa học có trên hệ thống.

#### Khóa học mẫu

| Khóa học | Trình độ | Số bài | Mô tả |
|----------|----------|--------|-------|
| **English for Beginners** | Beginner | 5 | Tiếng Anh cơ bản cho người mới bắt đầu |
| **Business English** | Intermediate | 5 | Tiếng Anh thương mại cho người đi làm |
| **Advanced Grammar** | Advanced | 5 | Ngữ pháp nâng cao |

#### Các action có thể thực hiện

- **🔍 Xem chi tiết**: Nhấn vào card khóa học
- **📝 Đăng ký**: Nhấn nút "Enroll" để ghi danh
- **📊 Xem tiến độ**: Thanh progress bar hiển thị % hoàn thành
- **🏷️ Lọc**: Lọc theo trình độ (Beginner/Intermediate/Advanced)

---

### 5. Chi tiết khóa học

**URL**: `http://localhost/courses/:id`

Hiển thị thông tin chi tiết của một khóa học.

#### Thông tin hiển thị

- **Tiêu đề**: Tên khóa học
- **Mô tả**: Nội dung chi tiết (hỗ trợ HTML)
- **Trình độ**: Beginner / Intermediate / Advanced
- **Số bài học**: Tổng số lessons
- **Thời lượng ước tính**: ~30 phút/bài
- **Tiến độ**: % đã hoàn thành (nếu đã đăng ký)

#### Danh sách bài học

Mỗi bài học hiển thị:
- 🔢 Số thứ tự (Order)
- 📌 Tiêu đề bài học
- ✅ Trạng thái: Đã hoàn thành / ⏳ Chưa học
- ⏱️ Thời lượng ước tính
- ▶️ Nút **Bắt đầu học**

---

### 6. Xem bài học

**URL**: `http://localhost/courses/:courseId/lessons/:lessonId`

Giao diện học tập chính.

#### Nội dung bài học

- **Tiêu đề bài học** (h1)
- **Nội dung HTML**: Bài giảng được format đẹp (hỗ trợ hình ảnh, bảng, code)
- **Từ vựng liên quan**: Danh sách từ mới xuất hiện trong bài
- **Nút phát âm 🔊**: Nhấn vào bất kỳ từ nào để nghe phát âm

#### Tính năng phát âm (Text-to-Speech)

Sử dụng Web Speech API tích hợp sẵn trong trình duyệt:
- Nhấn vào từ tiếng Anh → nghe phát âm giọng Mỹ (en-US)
- Có thể điều chỉnh tốc độ phát âm
- Hỗ trợ phát âm cả câu hoặc đoạn văn

#### Các action

| Nút | Chức năng |
|-----|-----------|
| ✅ **Mark as Complete** | Đánh dấu đã hoàn thành bài học |
| ➡️ **Next Lesson** | Chuyển sang bài học kế tiếp |
| ⬅️ **Previous Lesson** | Quay lại bài học trước |
| 📝 **Take Quiz** | Làm quiz của khóa học |

---

### 7. Flashcard từ vựng

**URL**: `http://localhost/vocabulary`

Học từ vựng với flashcard tương tác — đây là tính năng nổi bật của ứng dụng.

#### Giao diện flashcard

```
MẶT TRƯỚC:                        MẶT SAU:
┌─────────────────────────┐      ┌─────────────────────────┐
│                         │      │                         │
│       BEAUTIFUL         │      │  (adj) Xinh đẹp, đẹp đẽ │
│    /ˈbjuːtɪfəl/         │      │                         │
│                         │      │  "She has a beautiful   │
│     🔊 Nhấn để nghe     │      │   smile."               │
│                         │      │                         │
│  [Nhấn để xem nghĩa]    │      │  Cô ấy có nụ cười      │
│                         │      │  xinh đẹp.              │
└─────────────────────────┘      └─────────────────────────┘
```

#### Hiệu ứng lật thẻ

- Click/tap vào thẻ → thẻ lật 180° với hiệu ứng 3D mượt mà
- Click lại → lật về mặt trước
- Animation duration: 0.6 giây

#### Các chế độ học

| Chế độ | Mô tả |
|--------|-------|
| 🎲 **Học ngẫu nhiên** | Lật qua các từ ngẫu nhiên |
| 📂 **Học theo chủ đề** | Lọc từ theo category |
| 🔄 **Spaced Repetition** | Ôn tập theo thuật toán lặp lại ngắt quãng |
| 🆕 **Chỉ từ mới** | Chỉ hiển thị từ chưa học |
| ⭐ **Từ khó** | Hiển thị từ đã đánh dấu khó |

#### Đánh giá mức độ thuộc (sau mỗi thẻ)

| Nút | Ý nghĩa | Tác động |
|-----|---------|----------|
| 😟 **Khó** | Chưa thuộc | Hiện lại sau 1 ngày |
| 😐 **Trung bình** | Nhớ một phần | Hiện lại sau 3 ngày |
| 😊 **Dễ** | Đã thuộc | Hiện lại sau 7 ngày |

#### Điều hướng

- ← **Previous**: Thẻ trước
- → **Next**: Thẻ tiếp theo
- 🔀 **Shuffle**: Xáo trộn thứ tự
- 🔊 **Pronounce**: Phát âm từ

---

### 8. Làm bài Quiz

**URL**: `http://localhost/quiz`

Kiểm tra kiến thức với 2 loại câu hỏi.

#### Loại 1: Trắc nghiệm (Multiple Choice)

```
Câu hỏi: What is the meaning of "UBIQUITOUS"?

○ A. Hiếm gặp
● B. Có mặt ở khắp mọi nơi  ← Đáp án đúng
○ C. Nguy hiểm
○ D. Thú vị
```

**Đặc điểm:**
- 4 lựa chọn A, B, C, D
- Chỉ có 1 đáp án đúng
- Hiển thị giải thích sau khi trả lời

#### Loại 2: Điền từ (Fill-in-the-blank)

```
Điền từ còn thiếu:

"She has a _____ smile that lights up the room."

┌──────────────────────────────┐
│ beautiful                    │
└──────────────────────────────┘

Gợi ý: Tính từ nghĩa là "xinh đẹp" (9 ký tự)
```

**Đặc điểm:**
- Input text field
- Có hint (gợi ý) nếu cần
- Không phân biệt hoa/thường

#### Quy trình làm quiz

```
Chọn quiz → Đọc câu hỏi → Trả lời → Câu tiếp theo → ... → Submit → Kết quả
```

#### Kết quả quiz

```
🎉 Chúc mừng! Bạn đã hoàn thành quiz "English Basics"

📊 Kết quả: 8/10 câu đúng (80%)
⭐ XP nhận được: +80 XP
🏆 Thời gian: 5 phút 30 giây

┌──────────────────────────────────────────┐
│ Chi tiết:                                │
│ ✅ Câu 1: Đúng                           │
│ ✅ Câu 2: Đúng                           │
│ ❌ Câu 3: Sai → Đáp án đúng: "happy"    │
│ ✅ Câu 4: Đúng                           │
│ ...                                      │
└──────────────────────────────────────────┘

[Về Dashboard]  [Làm lại]  [Quiz khác]
```

---

### 9. Trang cá nhân

**URL**: `http://localhost/profile`

Quản lý thông tin cá nhân và cài đặt.

#### Thông tin hiển thị

- 🖼️ **Avatar**: Ảnh đại diện (mặc định là chữ cái đầu)
- 👤 **Username**: Tên đăng nhập
- 📧 **Email**: Địa chỉ email
- 📛 **Full Name**: Họ và tên
- 📅 **Ngày tham gia**: Ngày tạo tài khoản
- 📊 **Thống kê nhanh**: XP, Level, Streak

#### Chỉnh sửa thông tin

| Trường | Có thể sửa? | Ghi chú |
|--------|-------------|---------|
| Full Name | ✅ | Cập nhật bất cứ lúc nào |
| Email | ✅ | Cần xác nhận email mới |
| Password | ✅ | Cần nhập mật khẩu cũ |
| Username | ❌ | Không thể thay đổi |

#### Lịch sử hoạt động

Hiển thị 10 hoạt động gần nhất:
- ✅ Hoàn thành bài học
- 📝 Làm quiz
- 📚 Học từ vựng
- 🏆 Đạt thành tích mới

---

## 👨‍💼 Quản trị viên

### Truy cập Admin Panel

**URL**: `http://localhost:8000/admin/`

### Tạo tài khoản admin

```bash
# Vào container backend
docker-compose exec backend bash

# Tạo superuser
python manage.py createsuperuser

# Nhập thông tin theo hướng dẫn:
# Username: admin
# Email: admin@example.com
# Password: (nhập mật khẩu)
# Password (again): (nhập lại)
```

### Các module quản lý

#### 👥 Users
- Xem danh sách người dùng
- Kích hoạt/vô hiệu hóa tài khoản
- Reset mật khẩu
- Xem thống kê từng user

#### 📚 Courses & Lessons
- Thêm/sửa/xóa khóa học
- Quản lý bài học (thêm, sửa, xóa, sắp xếp)
- Upload nội dung HTML cho bài học

#### 📖 Vocabulary (Words)
- Thêm từ vựng mới (word, definition, phonetic, example, category)
- Import từ file CSV
- Quản lý categories
- Tìm kiếm và lọc từ vựng

#### 📝 Quizzes & Questions
- Tạo quiz mới
- Thêm câu hỏi (Multiple Choice / Fill-in-the-blank)
- Xem kết quả và lịch sử làm quiz
- Thống kê quiz phổ biến nhất

#### 📊 User Progress
- Xem tiến độ học tập của từng user
- Thống kê toàn hệ thống
- Export báo cáo CSV

#### 📅 Daily Activities
- Xem hoạt động hàng ngày
- Phân tích xu hướng học tập

---

## 🔌 API Reference

### Authentication

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| `POST` | `/api/auth/register/` | Đăng ký tài khoản mới |
| `POST` | `/api/auth/login/` | Đăng nhập, trả về JWT tokens |
| `POST` | `/api/auth/refresh/` | Refresh access token |
| `GET` | `/api/auth/profile/` | Lấy thông tin user hiện tại |
| `PUT` | `/api/auth/profile/` | Cập nhật profile |
| `PATCH` | `/api/auth/profile/` | Cập nhật một phần profile |
| `GET` | `/api/auth/stats/` | Thống kê cá nhân |

### Courses

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| `GET` | `/api/courses/` | Danh sách tất cả khóa học |
| `GET` | `/api/courses/:id/` | Chi tiết 1 khóa học |
| `GET` | `/api/courses/:id/lessons/` | Bài học của khóa học |
| `GET` | `/api/lessons/:id/` | Chi tiết 1 bài học |
| `POST` | `/api/courses/:id/enroll/` | Đăng ký khóa học |

### Vocabulary

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| `GET` | `/api/vocabulary/` | Danh sách từ vựng |
| `GET` | `/api/vocabulary/:id/` | Chi tiết 1 từ vựng |
| `GET` | `/api/vocabulary/flashcards/` | Lấy flashcards để học |
| `POST` | `/api/vocabulary/:id/review/` | Đánh giá mức độ thuộc |
| `GET` | `/api/vocabulary/stats/` | Thống kê từ vựng |

### Quiz

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| `GET` | `/api/quiz/` | Danh sách quizzes |
| `GET` | `/api/quiz/:id/` | Chi tiết quiz + câu hỏi |
| `POST` | `/api/quiz/:id/start/` | Bắt đầu làm quiz |
| `POST` | `/api/quiz/:id/submit/` | Nộp bài và nhận kết quả |
| `GET` | `/api/quiz/attempts/` | Lịch sử làm quiz |

### Progress

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| `GET` | `/api/progress/stats/` | Thống kê tổng quan |
| `GET` | `/api/progress/activities/` | Hoạt động gần đây |
| `POST` | `/api/progress/track/` | Ghi nhận hoạt động |
| `GET` | `/api/progress/achievements/` | Danh sách thành tích |
| `GET` | `/api/progress/leaderboard/` | Bảng xếp hạng |

### Xem & test API trực tiếp

Truy cập Swagger UI để xem và test API ngay trên trình duyệt:
- **Swagger UI**: http://localhost:8000/swagger/
- **ReDoc**: http://localhost:8000/redoc/

---

## 🔧 Troubleshooting

### ❌ Lỗi 1: Docker Desktop không chạy

**Triệu chứng:**
```
unable to get image: failed to connect to the docker API
The system cannot find the file specified
```

**Giải pháp:**
```powershell
# Windows: Khởi động Docker Desktop
Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"

# Chờ 2-3 phút cho Docker khởi động hoàn toàn
# Kiểm tra: biểu tượng cá voi ở taskbar phải chuyển sang xanh lá

# Thử lại
docker-compose up --build
```

**Nếu vẫn không được:**
```powershell
# Restart WSL
wsl --shutdown

# Restart Docker service
net stop com.docker.service
net start com.docker.service
```

---

### ❌ Lỗi 2: Port đã được sử dụng

**Triệu chứng:**
```
Error: bind: address already in use
```

**Giải pháp:**
```bash
# Windows: Tìm process đang dùng port
netstat -ano | findstr :80
netstat -ano | findstr :8000

# Kill process (thay PID bằng số thực tế)
taskkill /PID <PID> /F

# Linux/macOS
lsof -i :80
kill -9 <PID>
```

**Hoặc thay đổi port trong `docker-compose.yml`:**
```yaml
services:
  frontend:
    ports:
      - "3000:80"  # Thay 80 → 3000
```

---

### ❌ Lỗi 3: Database connection failed

**Triệu chứng:**
```
django.db.utils.OperationalError: could not connect to server
```

**Giải pháp:**
```bash
# Kiểm tra PostgreSQL container
docker-compose ps postgres

# Restart PostgreSQL
docker-compose restart postgres

# Chờ 10 giây rồi restart backend
docker-compose restart backend
```

---

### ❌ Lỗi 4: Frontend không kết nối được Backend

**Triệu chứng:**
- Frontend load được nhưng API call fail
- Console lỗi: CORS error hoặc Network Error

**Giải pháp:**
```bash
# Kiểm tra CORS settings trong .env
CORS_ALLOWED_ORIGINS=http://localhost,http://localhost:80

# Xem backend logs
docker-compose logs backend | grep -i cors

# Restart backend
docker-compose restart backend
```

---

### ❌ Lỗi 5: Build image thất bại / Out of memory

**Triệu chứng:**
```
ERROR: failed to solve: failed to compute cache key
```

**Giải pháp:**
```bash
# Xóa cache Docker
docker system prune -a --volumes

# Tăng memory cho Docker Desktop
# Settings → Resources → Memory → 4GB+

# Build lại
docker-compose build --no-cache
docker-compose up
```

---

### ❌ Lỗi 6: Không đăng nhập được

**Giải pháp:**
1. Xóa browser cache và cookies cho `localhost`
2. Thử **Incognito/Private mode**
3. Kiểm tra backend logs: `docker-compose logs backend | grep -i auth`
4. Đảm bảo backend đang chạy: `docker-compose ps`

---

### ❌ Lỗi 7: Celery worker không hoạt động

**Triệu chứng:**
- Không nhận được daily reminder
- Background tasks không chạy

**Giải pháp:**
```bash
# Kiểm tra Celery container
docker-compose ps celery_worker

# Xem logs
docker-compose logs celery_worker

# Restart Celery
docker-compose restart celery_worker celery_beat
```

---

## ❓ FAQ

### Q1: Có thể chạy project mà không dùng Docker không?

**A:** Có, nhưng phức tạp hơn. Cần cài đặt thủ công:
- Python 3.11+ (với virtualenv)
- Node.js 18+ (với npm)
- PostgreSQL 14+
- Redis 7+

---

### Q2: Làm sao để reset toàn bộ dữ liệu?

**A:**
```bash
# Dừng và xóa tất cả containers + volumes (MẤT HẾT DATA!)
docker-compose down -v

# Build và chạy lại
docker-compose up --build
```

---

### Q3: Có thể thêm từ vựng hàng loạt không?

**A:** Có! Sử dụng Django admin hoặc chạy seed script:
```bash
# Vào container
docker-compose exec backend bash

# Chạy seed script (đã có sẵn 50 từ)
python manage.py seed_data

# Hoặc import từ CSV
python manage.py import_words --file words.csv
```

---

### Q4: Làm sao để backup database?

**A:**
```bash
# Backup
docker-compose exec postgres pg_dump -U postgres english_platform > backup_$(date +%Y%m%d).sql

# Restore
cat backup.sql | docker-compose exec -T postgres psql -U postgres english_platform
```

---

### Q5: Ứng dụng có hỗ trợ dark mode không?

**A:** Có! Chuyển đổi theme tại trang Profile hoặc nhấn icon 🌙/☀️ ở header.

---

### Q6: Làm sao để deploy lên production?

**A:** Các tùy chọn phổ biến:
- **Frontend**: Vercel, Netlify, Cloudflare Pages
- **Backend**: Railway, Render, AWS ECS, DigitalOcean
- **Database**: Railway PostgreSQL, AWS RDS, Supabase

---

### Q7: Có API cho mobile app không?

**A:** Có! Tất cả API đều là RESTful JSON. Bạn có thể dùng cho:
- React Native (iOS/Android)
- Flutter
- Swift/Kotlin native apps

Xem docs tại: http://localhost:8000/swagger/

---

### Q8: Quên mật khẩu thì sao?

**A:** Hiện tại chưa có tính năng reset password tự động. Liên hệ admin hoặc:
```bash
# Reset password qua Django shell
docker-compose exec backend python manage.py changepassword <username>
```

---

### Q9: Dữ liệu mẫu có những gì?

**A:** Hệ thống seed sẵn:
- 👤 Không có user mặc định (cần đăng ký)
- 📚 3 khóa học (Beginner, Business, Advanced)
- 📖 15 bài học (5 bài/khóa)
- 📝 50 từ vựng phổ biến
- 🎮 3 quizzes với nhiều câu hỏi
- 🏆 10 achievements

---

### Q10: Ứng dụng có hỗ trợ mobile không?

**A:** Có! Giao diện được thiết kế **responsive**, hoạt động tốt trên:
- 📱 Mobile (320px+)
- 📱 Tablet (768px+)
- 💻 Desktop (1024px+)

---

## 📞 Hỗ trợ

Nếu gặp vấn đề không có trong hướng dẫn này:

- **GitHub Issues**: [Tạo issue mới](https://github.com/your-username/english-learning-app/issues)
- **Email**: toanld@example.com
- **Documentation**: Xem thêm trong folder `docs/`

---

## 📝 Changelog

### v1.0.0 (26/05/2026) — Initial Release
- ✨ Ra mắt phiên bản đầu tiên
- 📚 3 khóa học mẫu với 15 bài học
- 📝 50 từ vựng phổ biến
- 🎮 Hệ thống quiz với 2 loại câu hỏi
- 📊 Dashboard thống kê chi tiết với Recharts
- 🔊 Tính năng phát âm từ vựng (Web Speech API)
- 🏆 Hệ thống XP, Level, Streak, Achievements
- 🎴 Flashcard với hiệu ứng flip 3D
- 📱 Responsive design

---

**Cảm ơn bạn đã sử dụng English Learning Platform! 🎉**

*Made with ❤️ by ToànLD — 26/05/2026*
