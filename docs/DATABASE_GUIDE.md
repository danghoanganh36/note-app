# 🗄️ Hướng Dẫn Xem Database

## 🚀 Khởi Động Database

```bash
# Khởi động tất cả services (PostgreSQL + Redis + pgAdmin)
docker-compose up -d

# Kiểm tra status
docker-compose ps
```

---

## 🌐 Cách 1: Dùng pgAdmin (GUI - Đơn Giản Nhất)

### Bước 1: Mở pgAdmin
Truy cập: **http://localhost:5050**

### Bước 2: Đăng Nhập
- **Email**: `admin@example.com`
- **Password**: `admin`

### Bước 3: Kết Nối PostgreSQL
1. Click **"Add New Server"** (hoặc Object → Register → Server)
2. **General Tab**:
   - Name: `Handbook Database`
3. **Connection Tab**:
   - Host: `postgres` ⚠️ (KHÔNG phải localhost!)
   - Port: `5432`
   - Database: `handbook_compass`
   - Username: `postgres`
   - Password: `postgres`
4. Click **Save**

### Bước 4: Xem Dữ Liệu
- Servers → Handbook Database → Databases → handbook_compass → Schemas → public → Tables
- Right-click table → **View/Edit Data** → **All Rows**

---

## 💻 Cách 2: Dùng Terminal (psql)

### Kết Nối Database
```bash
# Vào container PostgreSQL
docker exec -it handbook_postgres psql -U postgres -d handbook_compass

# Hoặc từ máy local (nếu đã cài psql)
psql -h localhost -U postgres -d handbook_compass
# Password: postgres
```

### Các Lệnh Hữu Ích

```sql
-- Liệt kê tất cả tables
\dt

-- Xem cấu trúc table
\d users
\d documents

-- Query dữ liệu
SELECT * FROM users;
SELECT * FROM documents;
SELECT COUNT(*) FROM documents;

-- Xem database size
SELECT pg_size_pretty(pg_database_size('handbook_compass'));

-- Xem các indexes
\di

-- Thoát
\q
```

---

## 🛠️ Cách 3: Dùng GUI Apps (macOS)

### TablePlus (Recommended - Free Trial)
```bash
brew install --cask tableplus
```

**Cấu hình:**
- Host: `localhost`
- Port: `5432`
- User: `postgres`
- Password: `postgres`
- Database: `handbook_compass`

### Postico 2 (Paid - $49)
Download: https://eggerapps.at/postico2/

### DBeaver (Free & Open Source)
```bash
brew install --cask dbeaver-community
```

---

## 📊 Kiểm Tra Database Hiện Tại

```bash
# Xem tất cả tables
docker exec -it handbook_postgres psql -U postgres -d handbook_compass -c "\dt"

# Đếm số users
docker exec -it handbook_postgres psql -U postgres -d handbook_compass -c "SELECT COUNT(*) FROM users;"

# Đếm số documents
docker exec -it handbook_postgres psql -U postgres -d handbook_compass -c "SELECT COUNT(*) FROM documents;"
```

---

## 🔧 Thông Tin Kết Nối

| Service | Host | Port | Credentials |
|---------|------|------|-------------|
| **PostgreSQL** | `localhost` | `5432` | User: `postgres`<br>Pass: `postgres`<br>DB: `handbook_compass` |
| **pgAdmin** | `localhost` | `5050` | Email: `admin@example.com`<br>Pass: `admin` |
| **Redis** | `localhost` | `6379` | No password |

---

## 📝 Chạy Migrations

```bash
# Vào thư mục backend
cd backend

# Chạy migrations
alembic upgrade head

# Xem migration history
alembic history

# Tạo migration mới
alembic revision --autogenerate -m "Add new table"
```

---

## 🧹 Lệnh Docker Hữu Ích

```bash
# Xem logs
docker-compose logs postgres
docker-compose logs -f postgres  # Follow logs

# Restart service
docker-compose restart postgres

# Stop tất cả
docker-compose down

# Stop + xóa data (NGUY HIỂM!)
docker-compose down -v

# Backup database
docker exec handbook_postgres pg_dump -U postgres handbook_compass > backup.sql

# Restore database
docker exec -i handbook_postgres psql -U postgres handbook_compass < backup.sql
```

---

## 🎯 Quick Access Links

- **pgAdmin**: http://localhost:5050
- **Connection String**: `postgresql://postgres:postgres@localhost:5432/handbook_compass`
- **Redis**: `redis://localhost:6379`

---

## ⚠️ Troubleshooting

### Không kết nối được database?
```bash
# Kiểm tra container đang chạy
docker ps

# Kiểm tra logs
docker-compose logs postgres

# Restart
docker-compose restart postgres
```

### pgAdmin không load?
```bash
# Xem logs
docker-compose logs pgadmin

# Restart
docker-compose restart pgadmin
```

### Port 5432 đã được sử dụng?
```bash
# Kiểm tra process nào đang dùng port
lsof -i :5432

# Kill process (nếu cần)
kill -9 <PID>
```

---

## 🔐 Security Notes

⚠️ **CHÚ Ý**: Credentials mặc định CHỈ dùng cho development!

Khi deploy production:
1. Đổi password PostgreSQL
2. Đổi password pgAdmin
3. Dùng environment variables
4. Enable SSL/TLS
5. Restrict network access
