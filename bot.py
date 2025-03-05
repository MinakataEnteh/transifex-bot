import os
import time
import discord
import asyncio
import requests
from bs4 import BeautifulSoup

TOKEN = os.getenv("DISCORD_BOT_TOKEN")  # 環境変数からトークン取得
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))  # 環境変数からチャンネルID取得
TRANSIFEX_URL = "https://app.transifex.com/dailyroutines/dailyroutines/dashboard/"
last_checked_text = None

intents = discord.Intents.default()
client = discord.Client(intents=intents)

async def check_transifex_updates():
    global last_checked_text
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)

    while True:
        try:
            response = requests.get(TRANSIFEX_URL)
            if response.status_code != 200:
                await asyncio.sleep(300)
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            main_content = soup.get_text()

            if last_checked_text is None:
                last_checked_text = main_content
            elif last_checked_text != main_content:
                last_checked_text = main_content
                if channel:
                    await channel.send("🚀 Transifexが更新されました！\n🔗 " + TRANSIFEX_URL)

        except Exception as e:
            print(f"❌ エラー: {e}")

        await asyncio.sleep(300)

@client.event
async def on_ready():
    print(f"✅ ログイン成功: {client.user}")
    client.loop.create_task(check_transifex_updates())

client.run(TOKEN)
