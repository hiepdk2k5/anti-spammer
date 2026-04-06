# Discord Anti-Hack Bot

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Discord.py-2.3.2-blue?style=flat-square&logo=discord" alt="Discord.py">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
</p>

Bot bảo vệ server Discord khỏi bot spam bằng kênh bẫy (honeypot trap).

---

## 📋 Mục lục / Table of Contents

- [Tính năng / Features](#-tính-năng--features)
- [Cài đặt / Installation](#-cài-đặt--installation)
- [Triển khai / Deployment](#-triển-khai--deployment)
- [Giới hạn / Limits](#-giới-hạn--limits)

---

## ✨ Tính năng / Features

<details>
<summary><b>🇻🇳 Tiếng Việt (Click để mở)</b></summary>

- **Phát hiện bot spam**: Khi user vào kênh bẫy, bot tự động softban (ban + unban)
- **Xóa tin nhắn spam**: Xóa tất cả tin nhắn trong 3 giây gần nhất của user trên mọi kênh
- **Gửi DM thông báo**: Gửi link mời cho user bị kick để vào lại server
- **Whitelist role**: Bỏ qua các role được chỉ định (admin, mod, v.v.)
- **Tự động dọn cache**: Giới hạn cache 1000 users, tự động cleanup mỗi 60s

</details>

<details>
<summary><b>🇺🇸 English (Click to expand)</b></summary>

- **Spam bot detection**: When a user enters the trap channel, bot automatically softbans them (ban + unban)
- **Delete spam messages**: Deletes all messages from the user in the last 3 seconds across all channels
- **DM notification**: Sends an invite link to kicked users so they can rejoin
- **Whitelist roles**: Ignores specified roles (admin, mod, etc.)
- **Auto cache cleanup**: Limits cache to 1000 users, auto cleanup every 60s

</details>

---

## 🔧 Cài đặt / Installation

### 1. Tạo Bot Discord / Create Discord Bot

<details>
<summary><b>🇻🇳 Tiếng Việt</b></summary>

1. Vào [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" → đặt tên → Create
3. Vào tab "Bot" → Click "Add Bot"
4. Bật các Intent:
   - **MESSAGE CONTENT INTENT** (bắt buộc)
   - **SERVER MEMBERS INTENT** (bắt buộc)
5. Copy **Token** (sẽ dùng cho `BOT_TOKEN`)

</details>

<details>
<summary><b>🇺🇸 English</b></summary>

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" → name it → Create
3. Go to "Bot" tab → Click "Add Bot"
4. Enable Intents:
   - **MESSAGE CONTENT INTENT** (required)
   - **SERVER MEMBERS INTENT** (required)
5. Copy **Token** (for `BOT_TOKEN`)

</details>

### 2. Mời Bot / Invite Bot

<details>
<summary><b>🇻🇳 Tiếng Việt</b></summary>

Vào OAuth2 → URL Generator:
- Scopes: tick `bot`, `applications.commands`
- Bot Permissions:
  - ✅ Ban Members
  - ✅ Manage Messages
  - ✅ Read Messages/View Channels
  - ✅ Send Messages
  - ✅ Read Message History

Copy URL, paste vào browser, chọn server để mời.

</details>

<details>
<summary><b>🇺🇸 English</b></summary>

Go to OAuth2 → URL Generator:
- Scopes: tick `bot`, `applications.commands`
- Bot Permissions:
  - ✅ Ban Members
  - ✅ Manage Messages
  - ✅ Read Messages/View Channels
  - ✅ Send Messages
  - ✅ Read Message History

Copy URL, paste in browser, select server to invite.

</details>

### 3. Cấu hình .env / Configure .env

<details>
<summary><b>🇻🇳 Tiếng Việt</b></summary>

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
| `INVITE_LINK` | Link mời server | `https://discord.gg/abc123` |
| `IGNORED_ROLE_IDS` | Role whitelist, cách bằng dấu phẩy | `123,456,789` |

**Lấy Channel ID / Role ID:**
- Bật Developer Mode: User Settings → Advanced → Developer Mode ON
- Right-click kênh/role → Copy ID

</details>

<details>
<summary><b>🇺🇸 English</b></summary>

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
| `INVITE_LINK` | Server invite link | `https://discord.gg/abc123` |
| `IGNORED_ROLE_IDS` | Whitelist roles, comma-separated | `123,456,789` |

**Get Channel ID / Role ID:**
- Enable Developer Mode: User Settings → Advanced → Developer Mode ON
- Right-click channel/role → Copy ID

</details>

---

## 🚀 Triển khai / Deployment

### Chạy Local / Run Locally

<details>
<summary><b>🇻🇳 Tiếng Việt</b></summary>

```bash
# Clone repo
git clone https://github.com/yourusername/anti-spammer.git
cd anti-spammer

# Tạo virtual environment
python -m venv venv

# Cài dependencies
venv\Scripts\pip install -r requirements.txt

# Chạy bot
venv\Scripts\python main.py
```

</details>

<details>
<summary><b>🇺🇸 English</b></summary>

```bash
# Clone repo
git clone https://github.com/yourusername/anti-spammer.git
cd anti-spammer

# Create virtual environment
python -m venv venv

# Install dependencies
venv\Scripts\pip install -r requirements.txt

# Run bot
venv\Scripts\python main.py
```

</details>

---

## ⚙️ Cách hoạt động / How It Works

<details>
<summary><b>🇻🇳 Tiếng Việt</b></summary>

1. **Tạo kênh bẫy**: Đặt tên như `#bẫy-bot`, `#verify`, `#confirm`
2. **Giấu kênh**: Ẩn kênh khỏi @everyone (chỉ spam bot tò mò mới tìm thấy)
3. **Bot hoạt động**:
   - Theo dõi tin nhắn mọi kênh (lưu vào cache 3 giây)
   - Khi user vào kênh bẫy → softban ngay
   - Xóa 7 ngày tin nhắn + tin nhắn trong cache
   - Gửi DM với link mời

</details>

<details>
<summary><b>🇺🇸 English</b></summary>

1. **Create trap channel**: Name it `#trap-bot`, `#verify`, `#confirm`
2. **Hide channel**: Hide from @everyone (only curious spam bots will find it)
3. **Bot operation**:
   - Monitors messages in all channels (stores in 3-second cache)
   - When user enters trap channel → instant softban
   - Deletes 7 days of messages + messages in cache
   - Sends DM with invite link

</details>

---

## 📊 Giới hạn / Limits

<details>
<summary><b>🇻🇳 Tiếng Việt</b></summary>

| Thông số | Giá trị |
|----------|---------|
| Cache duration | 3 giây |
| Max messages/user | 5 tin |
| Max cache users | 1000 users |
| Cleanup interval | 60 giây |

</details>

<details>
<summary><b>🇺🇸 English</b></summary>

| Parameter | Value |
|-----------|-------|
| Cache duration | 3 seconds |
| Max messages/user | 5 messages |
| Max cache users | 1000 users |
| Cleanup interval | 60 seconds |

</details>

---

## 📝 License

MIT License - Free to use.
