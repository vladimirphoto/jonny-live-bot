import discord
import aiohttp
import os

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = int(os.getenv("TELEGRAM_CHAT_ID"))
DISCORD_CHANNEL_ID = 1498711867949056131

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ Бот запущен как {client.user}")
    print(f"Мониторит канал ID: {DISCORD_CHANNEL_ID}")

@client.event
async def on_message(message):
    print(f"📨 Получено сообщение из канала {message.channel.id}")  # для отладки
    
    if message.channel.id != DISCORD_CHANNEL_ID:
        return
    
    print(f"✅ Сообщение из нужного канала! Текст: {message.content[:100]}...")  # для отладки

    if "TikTok" not in message.content:
        print("❌ Нет слова TikTok — пропускаем")
        return

    text = f"""🚨 **Джонни в эфире!**

{message.content}"""

    try:
        async with aiohttp.ClientSession() as session:
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
            payload = {
                "chat_id": TELEGRAM_CHAT_ID,
                "text": text,
                "parse_mode": "Markdown"
            }
            async with session.post(url, json=payload) as resp:
                print(f"📤 Telegram ответил кодом: {resp.status}")
                if resp.status != 200:
                    print(await resp.text())
    except Exception as e:
        print(f"❌ Ошибка отправки: {e}")

client.run(DISCORD_TOKEN)
