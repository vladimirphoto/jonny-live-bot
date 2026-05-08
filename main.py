import discord
import aiohttp
import os

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

@client.event
async def on_message(message):
    if message.channel.id != DISCORD_CHANNEL_ID:
        return
    if "TikTok" not in message.content:
        return

    text = f"""🚨 **Джонни в эфире!**

{message.content}"""

    async with aiohttp.ClientSession() as session:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": text,
            "parse_mode": "Markdown"
        }
        await session.post(url, json=payload)
    
    print("✅ Отправлено в Telegram")

client.run(DISCORD_TOKEN)
