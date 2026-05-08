import discord
import aiohttp
import os
import sys

# Фикс для новых версий Python
if sys.version_info >= (3, 12):
    import collections.abc
    collections.abc.MutableMapping = collections.abc.MutableMapping

# ================== НАСТРОЙКИ ==================
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = int(os.getenv("TELEGRAM_CHAT_ID"))
DISCORD_CHANNEL_ID = 1498711867949056131

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ Бот успешно запущен как {client.user}")
    print(f"Мониторим канал: {DISCORD_CHANNEL_ID}")

@client.event
async def on_message(message):
    if message.channel.id != DISCORD_CHANNEL_ID:
        return
    
    # Только сообщения про TikTok Live
    if "TikTok" not in message.content and "live" not in message.content.lower():
        return

    # Красивое сообщение
    text = f"""🚨 **Джонни в эфире!**

{message.content}"""

    # Отправка в Telegram
    try:
        async with aiohttp.ClientSession() as session:
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
            payload = {
                "chat_id": TELEGRAM_CHAT_ID,
                "text": text,
                "parse_mode": "Markdown"
            }
            async with session.post(url, json=payload) as resp:
                if resp.status == 200:
                    print("✅ Успешно отправлено в Telegram")
                else:
                    print(f"❌ Ошибка Telegram: {resp.status}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

client.run(DISCORD_TOKEN)
