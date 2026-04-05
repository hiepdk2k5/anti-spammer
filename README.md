# Discord Anti-Hack Bot

Bot bảo vệ server Discord khỏi bot spam bằng cách sử dụng kênh bẫy (honeypot trap).

## Tính năng

- **Phát hiện bot spam**: Khi user vào kênh bẫy, bot tự động softban (ban + unban)
- **Xóa tin nhắn spam**: Xóa tất cả tin nhắn trong 3 giây gần nhất của user trên mọi kênh
- **Gửi DM thông báo**: Gửi link mời cho user bị kick để vào lại server
- **Whitelist role**: Bỏ qua các role được chỉ định (admin, mod, v.v.)
- **Tự động dọn cache**: Giới hạn cache 1000 users, tự động cleanup mỗi 60s

## Cài đặt

### 1. Tạo Bot Discord

1. Vào [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" → đặt tên → Create
3. Vào tab "Bot" → Click "Add Bot"
4. Bật các Intent:
   - **MESSAGE CONTENT INTENT** (bắt buộc)
   - **SERVER MEMBERS INTENT** (bắt buộc)
5. Copy **Token** (sẽ dùng cho `BOT_TOKEN`)

### 2. Mời Bot vào Server

Vào OAuth2 → URL Generator:
- Scopes: tick `bot`, `applications.commands`
- Bot Permissions:
  - ✅ Ban Members
  - ✅ Manage Messages
  - ✅ Read Messages/View Channels
  - ✅ Send Messages
  - ✅ Read Message History

Copy URL, paste vào browser, chọn server để mời.

### 3. Cấu hình .env

Tạo file `.env` trong thư mục gốc:

```env
BOT_TOKEN=your_bot_token_here
TRAP_CHANNEL_ID=1234567890123456789
INVITE_LINK=https://discord.gg/your-invite-link
IGNORED_ROLE_IDS=1234567890123456789,9876543210987654321
```

| Biến | Mô tả | Ví dụ |
|------|-------|-------|
| `BOT_TOKEN` | Token bot từ Developer Portal | `MTIzNDU2Nzg5MC4u.` |
| `TRAP_CHANNEL_ID` | ID kênh bẫy | `1234567890123456789` |
| `INVITE_LINK` | Link mời server (cho user bị kick) | `https://discord.gg/abc123` |
| `IGNORED_ROLE_IDS` | Các role được bỏ qua, phân cách bằng dấu phẩy | `123,456,789` |

#### Lấy Channel ID / Role ID

- Bật Developer Mode: User Settings → Advanced → Developer Mode ON
- Right-click kênh/role → Copy ID

### 4. Triển khai trên Render (Free)

1. Push code lên GitHub (không bao gồm file `.env`)
2. Vào [Render](https://render.com) → New Web Service
3. Connect GitHub repo
4. Cấu hình:
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
5. Thêm Environment Variables (từ file `.env`)
6. Click Create Web Service

### 5. Chạy Local (Test)

```bash
# Tạo virtual environment
python -m venv venv

# Windows
venv\Scripts\python main.py

# Linux/Mac
source venv/bin/activate
python main.py
```

## Cách hoạt động

1. **Tạo kênh bẫy**: Đặt tên như `#bẫy-bot`, `#verify`, `#confirm`
2. **Giấu kênh**: Ẩn kênh khỏi @everyone (chỉ spam bot tò mò mới tìm thấy)
3. **Bot hoạt động**:
   - Theo dõi tin nhắn mọi kênh (lưu vào cache 3 giây)
   - Khi user vào kênh bẫy → softban ngay
   - Xóa 7 ngày tin nhắn + tin nhắn trong cache
   - Gửi DM với link mời

## Giới hạn

| Thông số | Giá trị |
|----------|---------|
| Cache duration | 3 giây |
| Max messages/user | 5 tin |
| Max cache users | 1000 users |
| Cleanup interval | 60 giây |

## License

MIT License - Tự do sử dụng.
