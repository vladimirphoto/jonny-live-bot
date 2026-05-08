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
    print(f"✅ БОТ УСПЕШНО ЗАПУЩЕН КАК {client.user}")
    print(f"🎯 Мониторит канал: {DISCORD_CHANNEL_ID}")

@client.event
async def on_message(message):
    print(f"📨 Получено сообщение | Канал: {message.channel.id} | Автор: {message.author} | Текст: {message.content[:100]}")

    if message.channel.id != DISCORD_CHANNEL_ID:
        print("   → Пропущено: другой канал")
        return

    print("   → Это наш канал! Готовим отправку...")

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
                print(f"   → Telegram ответил: {resp.status}")
                if resp.status != 200:
                    print(await resp.text())
    except Exception as e:
        print(f"   ❌ Ошибка отправки: {e}")

    print("   → Обработка сообщения завершена\n")

client.run(DISCORD_TOKEN)
