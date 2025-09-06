import telebot
import requests
import os
import datetime

# =============================
# CONFIGURATION
# =============================
BOT_TOKEN = "8294178048:AAEN2wUg8hhefx6VHWuHnC38qUpfvop_FGI"
ADMIN_IDS = [8256977732, 8194709714]  # Admins list
API_KEY = "sk_live_e532d724903249c593e23d6198b329f47358ed34"
API_URL = "https://unexperienced-charis-unrailwayed.ngrok-free.app/api/mobile"

FORCE_JOIN_CHANNELS = [
    "https://t.me/+Y_M_LzKug1lmYTg1",  # GC link
    "https://t.me/monsters_support",
    "https://t.me/ShadowNestAPII"
]

bot = telebot.TeleBot(BOT_TOKEN)

# =============================
# STORAGE FILES
# =============================
CREDITS_FILE = "credits.txt"
LOG_FILE = "log.txt"
CLONE_LOG = "clone.txt"
REFERRAL_FILE = "referral.txt"
MUTED_FILE = "muted.txt"

# =============================
# HELPERS
# =============================
def load_data(filename):
    if not os.path.exists(filename):
        open(filename, "w").close()
    with open(filename, "r", encoding="utf-8") as f:
        return f.read().splitlines()

def save_data(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(map(str, data)))

def check_credits(user_id):
    credits = load_data(CREDITS_FILE)
    today = datetime.date.today().isoformat()
    for line in credits:
        uid, credit, date = line.split("|")
        if str(uid) == str(user_id):
            if date != today:
                return 5, today
            return int(credit), date
    return 5, today

def update_credits(user_id, new_credit, date):
    credits = load_data(CREDITS_FILE)
    updated = False
    for i in range(len(credits)):
        uid, credit, old_date = credits[i].split("|")
        if str(uid) == str(user_id):
            credits[i] = f"{user_id}|{new_credit}|{date}"
            updated = True
    if not updated:
        credits.append(f"{user_id}|{new_credit}|{date}")
    save_data(CREDITS_FILE, credits)

def is_muted(user_id):
    return str(user_id) in load_data(MUTED_FILE)

def mute_user(user_id):
    muted = load_data(MUTED_FILE)
    if str(user_id) not in muted:
        muted.append(str(user_id))
    save_data(MUTED_FILE, muted)

def unmute_user(user_id):
    muted = load_data(MUTED_FILE)
    if str(user_id) in muted:
        muted.remove(str(user_id))
    save_data(MUTED_FILE, muted)

# =============================
# FORCE JOIN CHECK
# =============================
def force_join_check(message):
    buttons = []
    for ch in FORCE_JOIN_CHANNELS:
        buttons.append([telebot.types.InlineKeyboardButton("👉 Join Channel", url=ch)])
    markup = telebot.types.InlineKeyboardMarkup(buttons)
    bot.send_message(
        message.chat.id,
        "⚠️ Please join our community channels first to use this bot.",
        reply_markup=markup
    )

# =============================
# START COMMAND / MENU
# =============================
@bot.message_handler(commands=['start'])
def start(message):
    if is_muted(message.from_user.id):
        bot.reply_to(message, "⛔ You are muted for 1 day.")
        return

    force_join_check(message)

    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🔍 SEARCH", "😇 MY PROFILE")
    markup.add("🤖 BOT CLONE", "🛠 SUPPORT")
    bot.send_message(
        message.chat.id,
        "👋 𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐓𝐎 𝐑𝐔𝐃𝐎-𝐈𝐍𝐅𝐎 𝐁𝐎𝐓\nPlease choose an option below:",
        reply_markup=markup
    )

# =============================
# SEARCH OPTION
# =============================
@bot.message_handler(func=lambda m: m.text == "🔍 SEARCH")
def search_start(message):
    bot.send_message(message.chat.id, "📱 Enter number without +91 (e.g. 7202936606)")
    bot.register_next_step_handler(message, do_search)

def do_search(message):
    user_id = message.from_user.id
    if is_muted(user_id):
        bot.reply_to(message, "⛔ You are muted for 1 day.")
        return

    credits, today = check_credits(user_id)
    if credits <= 0:
        mute_user(user_id)
        bot.reply_to(message, "⚠️ Daily search limit reached. You are muted for 1 day.")
        return

    number = message.text.strip()
    if not number.isdigit():
        bot.reply_to(message, "❌ Invalid format. Digits only without +91.")
        return

    try:
        res = requests.get(f"{API_URL}?api_key={API_KEY}&mobile={number}", timeout=10).json()
        if not res.get("success"):
            bot.reply_to(message, f"⚠️ API returned error: {res.get('message')}")
            return

        data_list = res.get("data", [])
        if not data_list:
            bot.reply_to(message, "❌ No record found.")
            return

        msg = f"📱 𝐑𝐞𝐬𝐮𝐥𝐭 for {number}:\n\n"
        for idx, record in enumerate(data_list, start=1):
            msg += f"{idx}️⃣ Record:\n"
            msg += f"• 👤 Name: {record.get('name','N/A')}\n"
            if record.get('fname'):
                msg += f"• 🧑 Father Name: {record.get('fname')}\n"
            msg += f"• 🏠 Address: {record.get('address','N/A')}\n"
            msg += f"• 📍 Circle: {record.get('circle','N/A')}\n"
            msg += f"• 🔎 Found In: {record.get('found_in','N/A')}\n\n"

        bot.send_message(user_id, msg)  # Only user sees, even in GC

        update_credits(user_id, credits - 1, today)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"{user_id} searched {number} at {datetime.datetime.now()}\n")

    except Exception as e:
        bot.reply_to(message, f"❌ API Error: {e}")

# =============================
# MY PROFILE
# =============================
@bot.message_handler(func=lambda m: m.text == "😇 MY PROFILE")
def my_profile(message):
    user_id = message.from_user.id
    credits, _ = check_credits(user_id)
    clone_count = len(load_data(CLONE_LOG))
    referral_link = f"https://t.me/YOUR_BOT?start={user_id}"

    msg = f"😇 𝐘𝐨𝐮𝐫 𝐏𝐫𝐨𝐟𝐢𝐥𝐞:\n\n"
    msg += f"• 👤 User ID: {user_id}\n"
    msg += f"• 💰 Credits: {credits}\n"
    msg += f"• 🤖 Clone Bots: {clone_count}\n"
    msg += f"• 🔗 Referral Link: {referral_link}\n"

    bot.reply_to(message, msg)

# =============================
# BOT CLONE
# =============================
@bot.message_handler(func=lambda m: m.text == "🤖 BOT CLONE")
def bot_clone(message):
    bot.send_message(message.chat.id, "⚠️ Enter your bot token to clone features (Example: 1234:ABC-XYZ)")
    bot.register_next_step_handler(message, process_clone)

def process_clone(message):
    token = message.text.strip()
    username = message.from_user.username or "NoUsername"
    with open(CLONE_LOG, "a", encoding="utf-8") as f:
        f.write(f"{username} | {token} at {datetime.datetime.now()}\n")
    bot.reply_to(message, "✅ Bot token saved. Clone features will run similarly to main bot.")

# =============================
# SUPPORT
# =============================
@bot.message_handler(func=lambda m: m.text == "🛠 SUPPORT")
def support(message):
    bot.reply_to(message, "🛠 For support contact: @RUDOWNER")

# =============================
# ADMIN COMMANDS
# =============================
@bot.message_handler(commands=['credit'])
def admin_credit(message):
    if message.from_user.id not in ADMIN_IDS:
        return
    try:
        _, amount, uid = message.text.split()
        update_credits(uid, int(amount), datetime.date.today().isoformat())
bot.reply_to(message, f"Credits updated! {amount} points added to user {uid}.")
