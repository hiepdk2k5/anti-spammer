<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Discord.py-2.3.2-blue?style=flat-square&logo=discord" alt="Discord.py">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
</p>

<h1 align="center">Discord Anti-Hack Bot</h1>

<p align="center">Bot bảo vệ server Discord khỏi bot spam bằng kênh bẫy (honeypot trap).</p>

<p align="center">
  <a href="#-features">English</a> •
  <a href="#-tính-năng">Tiếng Việt</a>
</p>

---

##  Features (English)

| Feature | Description |
|---------|-------------|
|  **Softban** | Ban + unban users entering trap channel, deletes 7 days of messages |
|  **Spam Cleanup** | Deletes spam messages from last 3 seconds across all channels |
|  **Notification** | Sends DM + invite link to kicked users |
|  **Whitelist** | Skips specified admin/mod roles |
|  **Auto Cleanup** | Limits to 1000 users, cleans every 60s |

### Setup

**1. Create Bot:**
- Go to [Discord Developer Portal](https://discord.com/developers/applications)
- New Application → Add Bot
- Enable **MESSAGE CONTENT INTENT** and **SERVER MEMBERS INTENT**
- Copy Token

**2. Invite Bot:**
- Scopes: `bot`, `applications.commands`
- Permissions: Ban Members, Manage Messages, Read Messages, Send Messages, Read Message History

**3. Config .env:**
```env
BOT_TOKEN=your_token_here
TRAP_CHANNEL_ID=1234567890123456789
INVITE_LINK=https://discord.gg/your-invite
IGNORED_ROLE_IDS=123456789,987654321
```

**4. Run:**
```bash
python -m venv venv
venv\Scripts\python main.py
```

### How it works
1. Create trap channel (e.g., `#bot-trap`) → Hide from @everyone
2. Bot monitors messages for 3 seconds
3. User enters trap → Softban + Delete spam + Send DM

### Limits
- Cache: 3 seconds, 5 messages/user, max 1000 users

---

##  Tính năng (Tiếng Việt)

| Tính năng | Mô tả |
|-----------|-------|
|  **Softban** | Ban + unban user vào kênh bẫy, xóa 7 ngày tin nhắn |
|  **Dọn spam** | Xóa tin nhắn spam trong 3 giây gần nhất trên mọi kênh |
|  **Thông báo** | Gửi DM + link mời cho user bị kick |
|  **Whitelist** | Bỏ qua các role admin/mod được chỉ định |
|  **Tự dọn cache** | Giới hạn 1000 users, cleanup mỗi 60s |

### Cài đặt

**1. Tạo Bot:**
- Vào [Discord Developer Portal](https://discord.com/developers/applications)
- New Application → Add Bot
- Bật **MESSAGE CONTENT INTENT** và **SERVER MEMBERS INTENT**
- Copy Token

**2. Mời Bot:**
- Scopes: `bot`, `applications.commands`
- Permissions: Ban Members, Manage Messages, Read Messages, Send Messages, Read Message History

**3. Config .env:**
```env
BOT_TOKEN=your_token_here
TRAP_CHANNEL_ID=1234567890123456789
INVITE_LINK=https://discord.gg/your-invite
IGNORED_ROLE_IDS=123456789,987654321
```

**4. Chạy:**
```bash
python -m venv venv
venv\Scripts\python main.py
```

### Cách hoạt động
1. Tạo kênh bẫy (VD: `#bot-trap`) → Ẩn khỏi @everyone
2. Bot theo dõi tin nhắn 3 giây
3. User vào kênh bẫy → Softban + Xóa spam + Gửi DM

### Giới hạn
- Cache: 3 giây, 5 tin/user, tối đa 1000 users

---

## 📜 License

MIT License - Free to use.
