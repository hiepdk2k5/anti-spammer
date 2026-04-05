import discord
import os
import time
import asyncio
import logging
from datetime import datetime
from dotenv import load_dotenv
from keep_alive import keep_alive

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

recent_messages = {}
CACHE_DURATION = 3
MAX_MESSAGES_PER_USER = 5
MAX_CACHE_USERS = 1000

async def cleanup_cache_task():
    while True:
        await asyncio.sleep(60)
        try:
            current_time = time.time()
            removed_users = 0
            
            users_to_remove = []
            for user_id, messages in list(recent_messages.items()):
                recent_messages[user_id] = [
                    (ts, msg_id, ch_id) for ts, msg_id, ch_id in messages 
                    if current_time - ts <= CACHE_DURATION
                ]
                if not recent_messages[user_id]:
                    users_to_remove.append(user_id)
            
            for user_id in users_to_remove:
                recent_messages.pop(user_id, None)
                removed_users += 1
            
            if removed_users > 0:
                logger.info(f'[CLEANUP] Đã xóa {removed_users} user, còn {len(recent_messages)} users trong cache')
        except Exception as e:
            logger.error(f'[CLEANUP ERROR] {e}')

def add_to_cache(user_id, message_id, channel_id):
    global recent_messages
    
    if len(recent_messages) >= MAX_CACHE_USERS and user_id not in recent_messages:
        oldest_user = min(recent_messages.keys(), key=lambda k: recent_messages[k][0][0] if recent_messages[k] else float('inf'))
        recent_messages.pop(oldest_user, None)
        logger.warning(f'[CACHE FULL] Xóa user {oldest_user} (cache đạt giới hạn {MAX_CACHE_USERS})')
    
    if user_id not in recent_messages:
        recent_messages[user_id] = []
    
    current_time = time.time()
    recent_messages[user_id].append((current_time, message_id, channel_id))
    recent_messages[user_id] = [
        (ts, msg_id, ch_id) for ts, msg_id, ch_id in recent_messages[user_id] 
        if current_time - ts <= CACHE_DURATION
    ][-MAX_MESSAGES_PER_USER:]

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')
INVITE_LINK = os.getenv('INVITE_LINK', '')

trap_channel_str = os.getenv('TRAP_CHANNEL_ID', '')
if not trap_channel_str:
    logger.error('[FATAL] TRAP_CHANNEL_ID không được để trống trong .env')
    TRAP_CHANNEL_ID = None
else:
    try:
        TRAP_CHANNEL_ID = int(trap_channel_str)
    except ValueError:
        logger.error(f'[FATAL] TRAP_CHANNEL_ID phải là số nguyên, nhận được: {trap_channel_str}')
        TRAP_CHANNEL_ID = None

IGNORED_ROLE_IDS_STR = os.getenv('IGNORED_ROLE_IDS', '')
if IGNORED_ROLE_IDS_STR:
    try:
        IGNORED_ROLE_IDS = [int(x.strip()) for x in IGNORED_ROLE_IDS_STR.split(',') if x.strip()]
    except ValueError:
        logger.warning('[WARN] IGNORED_ROLE_IDS không hợp lệ, dùng danh sách rỗng')
        IGNORED_ROLE_IDS = []
else:
    IGNORED_ROLE_IDS = []

logger.info(f'[CONFIG] TRAP_CHANNEL_ID: {TRAP_CHANNEL_ID}')
logger.info(f'[CONFIG] IGNORED_ROLE_IDS: {IGNORED_ROLE_IDS}')
logger.info(f'[CONFIG] INVITE_LINK: {"Có" if INVITE_LINK else "Không"}')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    logger.info(f'Đã đăng nhập thành công với tên {client.user}')
    
    if TRAP_CHANNEL_ID is None:
        logger.error('[FATAL] Bot không thể hoạt động vì thiếu TRAP_CHANNEL_ID hợp lệ')
        await client.close()
        return
    
    client.loop.create_task(cleanup_cache_task())
    logger.info('[SYSTEM] Đã khởi động cache cleanup task')

@client.event
async def on_message(message):
    if message.author.bot:
        return
    
    if TRAP_CHANNEL_ID is None:
        return
    
    user_id = message.author.id
    
    if message.channel.id != TRAP_CHANNEL_ID:
        add_to_cache(user_id, message.id, message.channel.id)
        return
    
    await handle_trap_channel(message)

async def send_dm_safely(user, message_content):
    try:
        await user.send(message_content)
        logger.info(f'[DM SENT] Đã gửi DM cho {user}')
        return True
    except discord.Forbidden:
        logger.warning(f'[DM FAILED] Không thể gửi DM cho {user} (chặn DM hoặc không share server)')
    except Exception as e:
        logger.error(f'[DM ERROR] Lỗi gửi DM cho {user}: {e}')
    return False

async def safe_delete_message(channel, message_id, retries=3):
    for attempt in range(retries):
        try:
            msg = await channel.fetch_message(message_id)
            await msg.delete()
            return True
        except discord.NotFound:
            return False
        except discord.Forbidden:
            logger.warning(f'[DELETE] Không có quyền xóa tin nhắn {message_id}')
            return False
        except discord.HTTPException as e:
            if e.status == 429:
                wait_time = e.retry_after if hasattr(e, 'retry_after') else 1
                logger.warning(f'[RATE LIMIT] Chờ {wait_time}s')
                await asyncio.sleep(wait_time)
            else:
                logger.error(f'[HTTP ERROR] {e}')
                return False
        except Exception as e:
            logger.error(f'[DELETE ERROR] {e}')
            if attempt < retries - 1:
                await asyncio.sleep(0.5)
    return False

async def safe_ban_member(guild, member, delete_seconds=604800, retries=3):
    for attempt in range(retries):
        try:
            await guild.ban(
                member, 
                delete_message_seconds=delete_seconds, 
                reason='Hệ thống Anti-Hack: Dính bẫy Bot'
            )
            return True
        except discord.Forbidden:
            logger.error(f'[BAN FORBIDDEN] Không có quyền ban {member}')
            return False
        except discord.HTTPException as e:
            if e.status == 429:
                wait_time = e.retry_after if hasattr(e, 'retry_after') else 1
                logger.warning(f'[BAN RATE LIMIT] Chờ {wait_time}s')
                await asyncio.sleep(wait_time)
            else:
                logger.error(f'[BAN HTTP ERROR] {e}')
                if attempt < retries - 1:
                    await asyncio.sleep(1)
    return False

async def safe_unban_member(guild, user, retries=5):
    for attempt in range(retries):
        try:
            await guild.unban(
                user, 
                reason='Softban: Đã dọn dẹp, cho phép vào lại'
            )
            return True
        except discord.NotFound:
            return True
        except discord.Forbidden:
            logger.error(f'[UNBAN FORBIDDEN] Không có quyền unban {user}')
            return False
        except discord.HTTPException as e:
            if e.status == 429:
                wait_time = e.retry_after if hasattr(e, 'retry_after') else 2 ** attempt
                logger.warning(f'[UNBAN RATE LIMIT] Chờ {wait_time}s (attempt {attempt+1}/{retries})')
                await asyncio.sleep(wait_time)
            else:
                logger.error(f'[UNBAN HTTP ERROR] {e}')
                await asyncio.sleep(1)
    return False

async def handle_trap_channel(message):
    user = message.author
    guild = message.guild
    user_id = user.id
    
    logger.info(f'[TRAP] Phát hiện {user} vào kênh bẫy')
    
    user_role_ids = [role.id for role in user.roles]
    if any(role_id in IGNORED_ROLE_IDS for role_id in user_role_ids):
        logger.info(f'[WHITELIST] Bỏ qua Softban cho {user} vì có Role quản trị')
        return
    
    bot_member = guild.me
    if not bot_member.guild_permissions.ban_members:
        logger.error(f'[PERMISSION] Bot không có quyền BAN_MEMBERS')
        return
    if not bot_member.guild_permissions.manage_messages:
        logger.warning(f'[PERMISSION] Bot không có quyền MANAGE_MESSAGES')
    
    if bot_member.top_role <= user.top_role:
        logger.error(f'[HIERARCHY] Role của bot ({bot_member.top_role}) không cao hơn user ({user.top_role})')
        return
    
    deleted_count = await delete_user_recent_messages(user_id, guild)
    logger.info(f'[DELETE] Đã xóa {deleted_count} tin nhắn spam của {user}')
    
    dm_sent = False
    if INVITE_LINK:
        dm_content = (
            "Bạn đã bị hệ thống Anti-Hack phát hiện và tạm thời xóa khỏi server.\n\n"
            "Nếu bạn là người dùng bình thường (không phải bot spam), "
            "vui lòng sử dụng link sau để tham gia lại server:\n"
            f"{INVITE_LINK}\n\n"
            "Xin lỗi vì sự bất tiện này."
        )
        dm_sent = await send_dm_safely(user, dm_content)
    
    ban_success = await safe_ban_member(guild, user)
    if not ban_success:
        logger.error(f'[BAN FAILED] Không thể ban {user}')
        return
    
    logger.info(f'[BAN] Đã ban {user}')
    
    unban_success = await safe_unban_member(guild, user)
    if not unban_success:
        logger.error(f'[UNBAN FAILED] CRITICAL: {user} ĐANG BỊ BAN VĨNH VIỄN! Cần unban thủ công!')
        return
    
    logger.info(f'[SUCCESS] Đã Softban {user} và xóa {deleted_count} tin nhắn spam (DM: {dm_sent})')
    
    try:
        await message.delete()
    except Exception as e:
        logger.warning(f'[DELETE TRAP] Không thể xóa tin nhắn trong kênh bẫy: {e}')

async def delete_user_recent_messages(user_id, guild):
    deleted = 0
    current_time = time.time()
    
    if user_id not in recent_messages:
        return deleted
    
    messages_to_delete = [
        (ts, msg_id, ch_id) for ts, msg_id, ch_id in recent_messages[user_id] 
        if current_time - ts <= CACHE_DURATION
    ]
    
    for ts, msg_id, ch_id in messages_to_delete:
        channel = guild.get_channel(ch_id)
        if channel:
            if await safe_delete_message(channel, msg_id):
                deleted += 1
        await asyncio.sleep(0.1)
    
    recent_messages.pop(user_id, None)
    return deleted

@client.event
async def on_error(event, *args, **kwargs):
    logger.error(f'[DISCORD ERROR] Event: {event}, Args: {args}', exc_info=True)

@client.event
async def on_disconnect():
    logger.warning('[DISCONNECT] Bot mất kết nối với Discord')

@client.event
async def on_resumed():
    logger.info('[RESUMED] Bot đã kết nối lại với Discord')

if __name__ == '__main__':
    if not TOKEN:
        logger.error('[FATAL] BOT_TOKEN không được để trống trong .env')
        exit(1)
    
    keep_alive()
    
    try:
        client.run(TOKEN, log_handler=None)
    except discord.LoginFailure:
        logger.error('[FATAL] Token Discord không hợp lệ')
        exit(1)
    except Exception as e:
        logger.error(f'[FATAL] Lỗi khởi động bot: {e}')
        exit(1)