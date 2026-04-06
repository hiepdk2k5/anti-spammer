<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Discord.py-2.3.2-blue?style=flat-square&logo=discord" alt="Discord.py">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
</p>

Bot bảo vệ server Discord khỏi bot spam bằng kênh bẫy (honeypot trap).

---

<details>
<summary><b>🇻🇳 Tiếng Việt (Click để mở)</b></summary>

# Discord Anti-Hack Bot

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

### 4. Triển khai

**Chạy Local:**

```bash
python -m venv venv
venv\Scripts\python main.py
```

**Hoặc Deploy trên các nền tảng:**
- Railway, Render, Fly.io, Koyeb, v.v.

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

</details>

---

<details>
<summary><b>🇬🇧 English (Click to expand)</b></summary>

# Discord Anti-Hack Bot

A Discord bot that protects your server from spam bots using a honeypot trap channel.

## Features

- **Bot Detection**: Automatically softbans (ban + unban) users who enter the trap channel
- **Spam Cleanup**: Deletes all messages from the user within the last 3 seconds across all channels
- **DM Notification**: Sends an invite link to legitimate users who were kicked
- **Role Whitelist**: Skips specified roles (admins, mods, etc.)
- **Auto Cache Cleanup**: Limits cache to 1000 users, auto-cleans every 60 seconds

## Installation

### 1. Create a Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" → Name it → Create
3. Go to "Bot" tab → Click "Add Bot"
4. Enable Intents:
   - **MESSAGE CONTENT INTENT** (required)
   - **SERVER MEMBERS INTENT** (required)
5. Copy **Token** (will be used for `BOT_TOKEN`)

### 2. Invite Bot to Server

Go to OAuth2 → URL Generator:
- Scopes: tick `bot`, `applications.commands`
- Bot Permissions:
  - ✅ Ban Members
  - ✅ Manage Messages
  - ✅ Read Messages/View Channels
  - ✅ Send Messages
  - ✅ Read Message History

Copy URL, paste into browser, select server to invite.

### 3. Configure .env

Create `.env` file in root directory:

```env
BOT_TOKEN=your_bot_token_here
TRAP_CHANNEL_ID=1234567890123456789
INVITE_LINK=https://discord.gg/your-invite-link
IGNORED_ROLE_IDS=1234567890123456789,9876543210987654321
```

| Variable | Description | Example |
|----------|-------------|---------|
| `BOT_TOKEN` | Bot token from Developer Portal | `MTIzNDU2Nzg5MC4u.` |
| `TRAP_CHANNEL_ID` | Trap channel ID | `1234567890123456789` |
| `INVITE_LINK` | Server invite link (for kicked users) | `https://discord.gg/abc123` |
| `IGNORED_ROLE_IDS` | Whitelisted role IDs, comma-separated | `123,456,789` |

#### Getting Channel ID / Role ID

- Enable Developer Mode: User Settings → Advanced → Developer Mode ON
- Right-click channel/role → Copy ID

### 4. Deployment

**Run Locally:**

```bash
python -m venv venv
venv\Scripts\python main.py
```

**Or Deploy on Platforms:**
- Railway, Render, Fly.io, Koyeb, etc.

## How It Works

1. **Create Trap Channel**: Name it `#bot-trap`, `#verify`, `#honeypot`, etc.
2. **Hide Channel**: Hide from @everyone (only curious spam bots will find it)
3. **Bot Actions**:
   - Monitors messages in all channels (stores in 3-second cache)
   - When user enters trap channel → instant softban
   - Deletes 7 days of messages + cached messages
   - Sends DM with invite link

## Limits

| Parameter | Value |
|-----------|-------|
| Cache duration | 3 seconds |
| Max messages/user | 5 messages |
| Max cache users | 1000 users |
| Cleanup interval | 60 seconds |

</details>

---

## License

MIT License - Free to use.
