import telebot
import requests
import datetime
import os

# =============================
# CONFIG
# =============================
BOT_TOKEN = "8294178048:AAEF13gjFiP66X8dFmkTPfsX2W_rz_Sd2WA"
API_URL = "https://lively-giving-shark.ngrok-free.app/api/mobile?api_key=sk_live_05ff8c0f8ca141b68217557e8b3fdcef653142c0&mobile="
ADMIN_ID = 123456789  # <- apna Telegram ID yaha daalna
FORCE_JOIN_CHANNELS = [
    "https://t.me/monsters_support",
    "https://t.me/+odoR0KXyo_8yZjU1",
    "https://t.me/ShadowNestAPIII"
]

bot = telebot.TeleBot(BOT_TOKEN)

# =============================
# STORAGE FILES
# =============================
CREDITS_FILE = "credits.txt"
LOG_FILE = "log1.txt"
REFERRAL_FILE = "referrals.txt"
MUTED_FILE = "muted.txt"

# =============================
# HELPERS
# =============================
def load_data(filename):
    if not os.path.exists(filename):
        open(filename, "w").close()
    with open(filename, "r") as f:
        return f.read().splitlines()

def save_data(filename, data):
    with open(filename, "w") as f:
        f.write("\n".join(map(str, data)))

def check_credits(user_id):
    credits = load_data(CREDITS_FILE)
    for line in credits:
        uid, credit, date = line.split("|")
        if str(uid) == str(user_id):
            # reset daily credits
            today = datetime.date.today().isoformat()
            if date != today:
                return int(5), today
            return int(credit), date
    return 5, datetime.date.today().isoformat()

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
        buttons.append([telebot.types.InlineKeyboardButton("👉 Click to Join", url=ch)])
    markup = telebot.types.InlineKeyboardMarkup(buttons)
    bot.send_message(
        message.chat.id,
        "⚠️ Please join our community channels first to use this bot.",
        reply_markup=markup
    )

# =============================
# COMMANDS
# =============================

@bot.message_handler(commands=['start'])
def start(message):
    if is_muted(message.from_user.id):
        bot.reply_to(message, "⛔ You are muted for 1 day due to spam.")
        return

    force_join_check(message)

    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🔍 Search", "⚙️ Settings")
    markup.add("👥 Referral", "📩 Contact")
    bot.send_message(
        message.chat.id,
        "👋 Welcome! Use the menu below.",
        reply_markup=markup
    )

@bot.message_handler(func=lambda m: m.text == "📩 Contact")
def contact(message):
    bot.reply_to(message, "For balance & help contact: @RUDOWNER")

@bot.message_handler(func=lambda m: m.text == "👥 Referral")
def referral(message):
    bot.reply_to(message, "Refer your friends. When they join, you get +1 credit!")

@bot.message_handler(func=lambda m: m.text == "⚙️ Settings")
def settings(message):
    bot.reply_to(message, "⚙️ Settings will be available soon.")

@bot.message_handler(func=lambda m: m.text == "🔍 Search")
def search_start(message):
    bot.send_message(
        message.chat.id,
        "🔎 Please enter a number with country code (e.g. +919876543210)."
    )
    bot.register_next_step_handler(message, do_search)

def do_search(message):
    user_id = message.from_user.id

    if is_muted(user_id):
        bot.reply_to(message, "⛔ You are muted for 1 day due to spam.")
        return

    credits, today = check_credits(user_id)
    if credits <= 0:
        mute_user(user_id)
        bot.reply_to(message, "⚠️ Daily search limit reached. You are muted for 1 day.")
        return

    number = message.text.strip()
    if not number.startswith("+"):
        bot.reply_to(message, "❌ Invalid format. Use with country code (e.g. +91...).")
        return

    try:
        res = requests.get(API_URL + number).json()
        bot.reply_to(message, f"📌 Result: {res}")
    except:
        bot.reply_to(message, "❌ API Error.")

    with open(LOG_FILE, "a") as f:
        f.write(f"{user_id} searched {number} at {datetime.datetime.now()}\n")

    update_credits(user_id, credits - 1, today)

# =============================
# ADMIN COMMANDS
# =============================

@bot.message_handler(commands=['unmute'])
def unmute(message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        uid = message.text.split()[1]
        unmute_user(uid)
        bot.reply_to(message, f"✅ User {uid} unmuted.")
    except:
        bot.reply_to(message, "❌ Usage: /unmute <user_id>")

@bot.message_handler(commands=['broadcast'])
def broadcast(message):
    if message.from_user.id != ADMIN_ID:
        return
    text = message.text.replace("/broadcast", "").strip()
    if text:
        users = load_data(CREDITS_FILE)
        for u in users:
            uid = u.split("|")[0]
            try:
                bot.send_message(uid, f"📢 Broadcast:\n\n{text}")
            except:
                pass
        bot.reply_to(message, "✅ Broadcast sent.")

# =============================
# RUN
# =============================
print("🤖 Bot running...")
bot.infinity_polling()
