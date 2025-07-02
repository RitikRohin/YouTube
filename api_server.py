# File: key_bot.py

import uuid
import json
import os
from pyrogram import Client, filters

# 🛠️ Replace with your values from https://my.telegram.org
API_ID = 123456
API_HASH = "your_api_hash"
BOT_TOKEN = "your_bot_token"

KEY_FILE = "apikeys.json"

# 📁 If file doesn't exist, create empty
if not os.path.exists(KEY_FILE):
    with open(KEY_FILE, "w") as f:
        json.dump({}, f)

# 🔁 Load and Save Key Functions
def load_keys():
    with open(KEY_FILE, "r") as f:
        return json.load(f)

def save_keys(data):
    with open(KEY_FILE, "w") as f:
        json.dump(data, f, indent=2)

# 🚀 Bot Client
app = Client("key-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# 👋 Welcome Message
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("👋 Welcome!\nUse /getkey to generate your YouTube API Key.")

# 🔑 Generate or Get Key
@app.on_message(filters.command("getkey"))
async def getkey(client, message):
    user_id = str(message.from_user.id)
    keys = load_keys()

    if user_id in keys:
        await message.reply(f"🔑 Your API Key:\n`{keys[user_id]}`")
    else:
        new_key = uuid.uuid4().hex
        keys[user_id] = new_key
        save_keys(keys)
        await message.reply(f"✅ API Key Generated:\n`{new_key}`")

# 👁️ View Your Key
@app.on_message(filters.command("mykey"))
async def mykey(client, message):
    user_id = str(message.from_user.id)
    keys = load_keys()

    if user_id in keys:
        await message.reply(f"🔑 Your API Key:\n`{keys[user_id]}`")
    else:
        await message.reply("❌ You don’t have a key yet. Use /getkey")

# 🗑️ Revoke Key
@app.on_message(filters.command("revoke"))
async def revoke(client, message):
    user_id = str(message.from_user.id)
    keys = load_keys()

    if user_id in keys:
        del keys[user_id]
        save_keys(keys)
        await message.reply("🗑️ Your API Key has been revoked.")
    else:
        await message.reply("❌ You don’t have a key to revoke.")
print("run")
app.run()
