import uuid
import json
import os
from pyrogram import Client, filters

# ✅ Load environment variables
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

KEY_FILE = "apikeys.json"

# Create empty file if not exists
if not os.path.exists(KEY_FILE):
    with open(KEY_FILE, "w") as f:
        json.dump({}, f)

def load_keys():
    with open(KEY_FILE, "r") as f:
        return json.load(f)

def save_keys(data):
    with open(KEY_FILE, "w") as f:
        json.dump(data, f, indent=2)

app = Client("api-key-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("👋 Welcome!\nUse /getkey to get your API Key.")

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

@app.on_message(filters.command("mykey"))
async def mykey(client, message):
    user_id = str(message.from_user.id)
    keys = load_keys()

    if user_id in keys:
        await message.reply(f"🔑 Your API Key:\n`{keys[user_id]}`")
    else:
        await message.reply("❌ You don’t have a key yet. Use /getkey")

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


ADMIN_ID = 7666870729  # 🛡️ Change this to your Telegram user ID

@app.on_message(filters.command("allow") & filters.user(ADMIN_ID))
async def allow_user(client, message):
    if len(message.command) < 2:
        await message.reply("Usage: /allow <user_id>")
        return

    user_id = message.command[1]
    allowed = load_allowed()

    if user_id in allowed:
        await message.reply("✅ User already allowed.")
    else:
        allowed.append(user_id)
        save_allowed(allowed)
        await message.reply(f"✅ User {user_id} is now allowed.")

