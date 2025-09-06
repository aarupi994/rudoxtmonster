import telebot
import requests
import random
import string
import time

# Замените 'YOUR_BOT_TOKEN' на токен вашего бота
bot = telebot.TeleBot("YOUR_BOT_TOKEN")
CRYPTOBOT_API_KEY = "YOUR_API_TOKEN_CRYPTOBOT"
user_data = {
    "7381899082": {
        "tokens": 10000,
        "max_tokens": 10000,
        "token_regen": 0.1,
        "limit_results": 300,
        "requests_count": 29,
        "balance": 0.00,
        "withdrawal_funds": 0.00,
        "referrals": 0,
        "language": "ru",  
        "registration_date": "30.10.2024 18:29:09"
    }
}
def generate_api_key(user_id):
    letters = ''.join(random.choice(string.ascii_letters) for _ in range(2))
    digit = random.choice(string.digits)
    random_letters = ''.join(random.choice(string.ascii_letters) for _ in range(5))
    api_key = f"{user_id}:{letters}{digit}{random_letters}"
    return api_key
def generate_payment_link(user_id, currency):
    url = "https://pay.crypt.bot/api/createInvoice"
    headers = {
        "Crypto-Pay-API-Token": CRYPTOBOT_API_KEY
    }
    payload = {
        "asset": currency,  
        "amount": "1",  
        "description": f"Пополнение баланса для пользователя {user_id}",
        "payload": f"user_id_{user_id}"  
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        return data.get("result", {}).get("invoice_url")
    else:
        return None
def make_request(Term):
    API = "ТУТ АПИ ЛИК ОСИНТ"
    data = {"token": API, "request": Term, "limit": 100, "lang": "ru"}
    url = 'https://server.leakosint.com/'
    response = requests.post(url, json=data, verify=False)
    return response.json()
@bot.message_handler(commands=['start'])
def send_welcome(message):
    text = "🕵 Я могу искать практически всё. Просто отправь мне свой запрос."
    keyboard = telebot.types.InlineKeyboardMarkup()
    search_button = telebot.types.InlineKeyboardButton(text="🔍 Поиск", callback_data='search')
    info_button = telebot.types.InlineKeyboardButton(text="📋 Информация", callback_data='info')
    shop_button = telebot.types.InlineKeyboardButton(text="🛍 Магазин", callback_data='shop')
    keyboard.row(search_button, info_button, shop_button)
    settings_button = telebot.types.InlineKeyboardButton(text="⚙️ Настройки", callback_data='settings')
    menu_button = telebot.types.InlineKeyboardButton(text="🗃 Меню", callback_data='menu')
    keyboard.row(settings_button, menu_button)
    bot.send_message(message.chat.id, text, reply_markup=keyboard)
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        user_id = call.from_user.id  
        user_name = call.from_user.first_name  
        user_username = call.from_user.username 

        if call.data == 'search':
            search_text = (
                "Вы можете искать следующие данные:\n"
                "📧Поиск по почте\n"
                "├ example@gmail.com - поиск почты\n"
                "├ example@ - поиск без учёта домена\n"
                "└ @gmail.com - поиск определённых доменов.\n\n"
                "👤Поиск по имени или нику\n"
                "├ Петров\n"
                "├ Петров Максим\n"
                "├ Петров Сергеевич\n"
                "├ Максим Сергеевич\n"
                "├ Петров Максим Сергеевич\n"
                "└ ShadowPlayer228\n\n"
                "📱Поиск по номеру телефона\n"
                "├ +79002206090\n"
                "├ 79002206090\n"
                "└ 89002206090\n\n"
                "🔑Поиск по паролю\n"
                "└ 123qwe\n\n"
                "🚗Поиск по авто\n"
                "├ O999МУ777 - поиск авто по РФ\n"
                "├ ВО4561АХ - поиск авто по УК\n"
                "└ XTA21150053965897 - поиск по VIN\n\n"
                "✈Поиск телеграм-аккаунта\n"
                "├ Petrov Ivan - поиск по имени и фамилии\n"
                "├ 314159265 - поиск по ID аккаунта\n"
                "└ Petivan - поиск по юзернеиму. Собака перед юзернеимом не ставится!\n\n"
                "📘Поиск фейсбук-аккаунта\n"
                "├ Petrov Ivan - поиск по ФИО\n"
                "└ 314159265 - поиск по ID аккаунта\n\n"
                "🌟Поиск аккаунта ВКонтакте\n"
                "├ Petrov Ivan - поиск по имени и фамилии\n"
                "└ 314159265 - поиск по ID аккаунта\n\n"
                "🌟Поиск аккаунта Инстаграмм\n"
                "├ Petrov Ivan - поиск по имени и фамилии\n"
                "└ 314159265 - поиск по ID аккаунта\n\n"
                "🌟Поиск по IP\n"
                "└ 127.0.0.1\n\n"
                "📃Поиск по файлу. Кодировка UTF-8. Один запрос на каждой строке.\n\n"
                "Поддерживаются составные запросы в любых форматах:\n"
                "├ Петров 79002206090 \n"
                "├ Максим Сергеевич 127.0.0.1\n"
                "├ ShadowPlayer228 example@gmail.com\n"
                "├ Максим Сергеевич Москва\n"
                "├ example@gmail.com 123qwe\n"
                "└ ShadowPlayer228 16.08.1994\n\n"
                "Так же вы можете искать данные сразу по нескольким запросам. Для этого укажите каждый запрос на отдельной строке и они выполнятся одновременно."
            )
            back_keyboard = telebot.types.InlineKeyboardMarkup()
            back_button = telebot.types.InlineKeyboardButton(text="⬅️ Назад", callback_data='back_to_menu')
            back_keyboard.row(back_button)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=search_text, reply_markup=back_keyboard)

        elif call.data == 'settings':
            settings_keyboard = telebot.types.InlineKeyboardMarkup()
            language_button = telebot.types.InlineKeyboardButton(text="🌐 Язык", callback_data='language')
            notifications_button = telebot.types.InlineKeyboardButton(text="🔔 Уведомления", callback_data='notifications')
            back_button = telebot.types.InlineKeyboardButton(text="⬅️ Назад", callback_data='back_to_menu')
            settings_keyboard.row(language_button, notifications_button)
            settings_keyboard.row(back_button)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="⚙️ Настройки", reply_markup=settings_keyboard)

        elif call.data == 'language':
            language_text = (
                "Ваш текущий язык - «ru». Выберите новый язык в списке, либо используйте команду /language code.\n"
                "Вместо \"code\" нужно указать код любого языка, поддерживаемого Google-переводчиком. Список кодов можно найти вот тут: https://cloud.google.com/translate/docs/languages"
            )
            language_keyboard = telebot.types.InlineKeyboardMarkup()
            row1 = [telebot.types.InlineKeyboardButton(text="🇷🇺 Русский✔️", callback_data='lang_ru'),
                    telebot.types.InlineKeyboardButton(text="🇺🇦 Українська", callback_data='lang_uk'),
                    telebot.types.InlineKeyboardButton(text="🇧🇾 Беларуская", callback_data='lang_be')]
            row2 = [telebot.types.InlineKeyboardButton(text="🇬🇧 English", callback_data='lang_en'),
                    telebot.types.InlineKeyboardButton(text="🇩🇪 Deutsch", callback_data='lang_de'),
                    telebot.types.InlineKeyboardButton(text="🇫🇷 Français", callback_data='lang_fr')]
            row3 = [telebot.types.InlineKeyboardButton(text="🇹🇷 Türkçe", callback_data='lang_tr'),
                    telebot.types.InlineKeyboardButton(text="🇪🇸 Español", callback_data='lang_es'),
                    telebot.types.InlineKeyboardButton(text="🇮🇹 Italiano", callback_data='lang_it')]
            row4 = [telebot.types.InlineKeyboardButton(text="🇨🇳 中文", callback_data='lang_zh'),
                    telebot.types.InlineKeyboardButton(text="🇯🇵 日本語", callback_data='lang_ja'),
                    telebot.types.InlineKeyboardButton(text="🇰🇷 한국어", callback_data='lang_ko')]
            back_button = telebot.types.InlineKeyboardButton(text="⬅️ Назад", callback_data='back_to_settings')

            language_keyboard.row(*row1)
            language_keyboard.row(*row2)
            language_keyboard.row(*row3)
            language_keyboard.row(*row4)
            language_keyboard.row(back_button)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=language_text, reply_markup=language_keyboard)

        elif call.data.startswith('lang_'):
            selected_language = call.data.split('_')[1]
            user_data[str(user_id)]['language'] = selected_language  # Сохраняем выбранный язык
            bot.answer_callback_query(call.id, text=f"Язык изменен на {selected_language}")
            callback_inline(call)  
        elif call.data == 'notifications':
            notifications_text = "Выберите, какие уведомления нужно вам присылать"
            notifications_keyboard = telebot.types.InlineKeyboardMarkup()
            leak_button = telebot.types.InlineKeyboardButton(text="✅️ Новые утечки", callback_data='leak_notifications')
            news_button = telebot.types.InlineKeyboardButton(text="✅️ Новости", callback_data='news_notifications')
            referral_button = telebot.types.InlineKeyboardButton(text="✅️ Новые рефералы", callback_data='referral_notifications')
            refill_button = telebot.types.InlineKeyboardButton(text="✅️ Пополнения рефералов", callback_data='refill_notifications')
            back_button = telebot.types.InlineKeyboardButton(text="⬅️ Назад", callback_data='back_to_settings')
            notifications_keyboard.row(leak_button)
            notifications_keyboard.row(news_button)
            notifications_keyboard.row(referral_button)
            notifications_keyboard.row(refill_button)
            notifications_keyboard.row(back_button)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=notifications_text, reply_markup=notifications_keyboard)

        elif call.data == 'menu':
            menu_text = "Что вас интересует?"
            menu_keyboard = telebot.types.InlineKeyboardMarkup()
            file_search_button = telebot.types.InlineKeyboardButton(text="📝 Поиск по файлам", callback_data='file_search')
            api_button = telebot.types.InlineKeyboardButton(text="⚙️ API", callback_data='api')
            faq_button = telebot.types.InlineKeyboardButton(text="❓ Ответы на частые вопросы", callback_data='faq')
            db_list_button = telebot.types.InlineKeyboardButton(text="🗃 Список баз", callback_data='db_list')
            refill_balance_button = telebot.types.InlineKeyboardButton(text="💰 Пополнение баланса", callback_data='refill_balance')
            withdraw_button = telebot.types.InlineKeyboardButton(text="💳 Вывод средств", callback_data='withdraw')
            referral_system_button = telebot.types.InlineKeyboardButton(text="👥 Реферальная система", callback_data='referral_system')
            mirror_button = telebot.types.InlineKeyboardButton(text="🪞 Создать зеркало", callback_data='mirror')
            delete_button = telebot.types.InlineKeyboardButton(text="🚫 Удалить себя", callback_data='delete_self')
            back_button = telebot.types.InlineKeyboardButton(text="◀️ Назад", callback_data='back_to_menu')
            menu_keyboard.row(file_search_button, api_button)
            menu_keyboard.row(faq_button, db_list_button)
            menu_keyboard.row(refill_balance_button, withdraw_button)
            menu_keyboard.row(referral_system_button, mirror_button)
            menu_keyboard.row(delete_button)
            menu_keyboard.row(back_button)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=menu_text, reply_markup=menu_keyboard)

        elif call.data == 'file_search':
            file_search_text = (
                "💯 Наш сервис может выполнять сотни тысяч поисков за раз!\n\n"
                "📃 Просто отправьте ваши данные в виде текстового файла, в котором на каждой строке написан один запрос.\n"
                "✉ Бот выполнит их все и отправит вам результаты.\n"
                "👛 Цена выполнения такого поиска - 1$ за 1000 слов.\n\n"
                "🆓 Первая 1000 запросов бесплатно! Попробуйте."
            )
            back_keyboard = telebot.types.InlineKeyboardMarkup()
            back_button = telebot.types.InlineKeyboardButton(text="⬅️ Назад", callback_data='back_to_menu')
            back_keyboard.row(back_button)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=file_search_text, reply_markup=back_keyboard)

        elif call.data == 'api':
            api_key = generate_api_key(user_id)
            api_text = (
                "⚙ Вы можете пользоваться нашим сервисом через API.\n"
                f"🔑 Вот ваш персональный API-ключ, держите его в секрете:\n{api_key}"
            )
            api_keyboard = telebot.types.InlineKeyboardMarkup()
            change_api_button = telebot.types.InlineKeyboardButton(text="🖊 Изменить API-ключ", callback_data='change_api_key')
            docs_button = telebot.types.InlineKeyboardButton(text="Документация", url="https://leakosint.com/api")
            back_button = telebot.types.InlineKeyboardButton(text="⬅️ Назад", callback_data='back_to_menu')
            api_keyboard.row(change_api_button, docs_button)
            api_keyboard.row(back_button)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=api_text, reply_markup=api_keyboard)

        elif call.data == 'change_api_key':
            new_api_key = generate_api_key(user_id)
            new_api_text = (
                "⚙ Вы можете пользоваться нашим сервисом через API.\n"
                f"🔑 Вот ваш новый персональный API-ключ, держите его в секрете:\n{new_api_key}"
            )
            api_keyboard = telebot.types.InlineKeyboardMarkup()
            change_api_button = telebot.types.InlineKeyboardButton(text="🖊 Изменить API-ключ", callback_data='change_api_key')
            docs_button = telebot.types.InlineKeyboardButton(text="Документация", url="https://leakosint.com/api")
            back_button = telebot.types.InlineKeyboardButton(text="⬅️ Назад", callback_data='back_to_menu')
            api_keyboard.row(change_api_button, docs_button)
            api_keyboard.row(back_button)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=new_api_text, reply_markup=api_keyboard)

        elif call.data == 'db_list':
            db_list_text = (
                "💧 На данный момент в наш бот загружено 3017 утечек.\n"
                "✏️ Суммарно в них содержится 69.188.427.028 записей.\n"
                "😲 Это больше, чем в любом другом телеграм-боте!\n\n"
                "🔎 Для поиска доступны следующие данные:\n"
                "📩Email:                   24.335.322.638\n"
                "👤ФИО:                     11.236.237.607\n"
                "🔑Пароль:                  11.161.673.768\n"
                "📞Телефон:                 9.324.230.153\n"
                "👤Ник:                     4.826.634.160\n"
                "🃏Номер документа:         3.009.829.885\n"
                "🆔VK ID:                   1.819.611.354\n"
                "ⓕFacebookID:               829.607.856\n"
                "🎯IP:                      684.733.772\n"
                "🔢SSN:                     651.615.996\n"
                "🚘Автомобильный номер:     405.358.873\n"
                "🔗Ссылка:                  319.497.568\n"
                "🏢Название компании:       299.564.297\n"
                "✈TelegramID:              154.974.753\n"
                "🌐Домен:                   84.443.741\n"
                "📷Идентификатор Instagram: 45.090.607"
            )
            db_list_keyboard = telebot.types.InlineKeyboardMarkup()
            full_list_button = telebot.types.InlineKeyboardButton(text="💦 Полный список утечек", callback_data='full_db_list')
            back_button = telebot.types.InlineKeyboardButton(text="⬅️ Назад", callback_data='back_to_menu')
            db_list_keyboard.row(full_list_button)
            db_list_keyboard.row(back_button)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=db_list_text, reply_markup=db_list_keyboard)

        elif call.data == 'full_db_list':
            with open("database_list.html", "rb") as file:
                bot.send_document(call.message.chat.id, file, caption="❗ Обратите внимание, что количество записей в утечке может не соответствовать количеству записей в описании. Это происходит из-за того, что иногда мы индексируем несколько версий одной и той же базы. Например, оригинальный файл и версию с расшифрованными паролями. Так же базы могут состоять из нескольких таблиц (например, пользователи и заказы), что так же увеличивает количество записей.")

        elif call.data == 'refill_balance':
            refill_text = "💸 Выберите способ оплаты"
            refill_keyboard = telebot.types.InlineKeyboardMarkup()
            usdt_button = telebot.types.InlineKeyboardButton(text="⚪ USDT", callback_data='refill_usdt')
            ton_button = telebot.types.InlineKeyboardButton(text="🟣 TON", callback_data='refill_ton')
            solana_button = telebot.types.InlineKeyboardButton(text="🟢 Solana", callback_data='refill_solana')
            bitcoin_button = telebot.types.InlineKeyboardButton(text="🔴 Bitcoin", callback_data='refill_bitcoin')
            back_button = telebot.types.InlineKeyboardButton(text="⬅️ Назад", callback_data='back_to_menu')
            refill_keyboard.row(usdt_button, ton_button)
            refill_keyboard.row(solana_button, bitcoin_button)
            refill_keyboard.row(back_button)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=refill_text, reply_markup=refill_keyboard)

        elif call.data.startswith('refill_'):
            currency = call.data.split('_')[1].upper()
            payment_link = generate_payment_link(user_id, currency)

            if payment_link:
                payment_text = (
                    f"👛 Используйте адрес ниже для пополнения баланса.\n\n"
                    f"Монета: 🪶 {currency}\n\n"
                    f"{payment_link}\n\n"
                    f"💳 Вы можете перевести любую сумму на эту ссылку. Она будет зачислена на ваш баланс без комиссий.\n\n"
                    f"⚠️Данная ссылка будет действовать ещё 60 минут."
                )
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=payment_text)
            else:
                bot.answer_callback_query(call.id, text="Ошибка при генерации ссылки на оплату. Попробуйте позже.")

        elif call.data == 'back_to_settings':
            callback_inline(call)

        elif call.data == 'back_to_menu':
            send_welcome(call.message)

        elif call.data == 'withdraw':
            user_balance = user_data.get(str(user_id), {}).get("balance", 0.00)

            withdraw_text = (
                "Минимальная сумма для вывода 5$\n"
                f"💱 Ваш текущий баланс для вывода: {user_balance}$ ( {user_balance * 103.6} ₽ )\n"  # Пример конвертации в рубли
                "💵 Обратите внимание, что выводить можно только деньги, заработанные за пополнения ваших рефералов."
            )

            withdraw_keyboard = telebot.types.InlineKeyboardMarkup()
            bank_card_button = telebot.types.InlineKeyboardButton(text="💳 Банковская карта", callback_data='withdraw_bank_card')
            cryptobot_button = telebot.types.InlineKeyboardButton(text="👛 CryptoBot", callback_data='withdraw_cryptobot')
            referral_system_button = telebot.types.InlineKeyboardButton(text="👥 Реферальная система", c    markup.add("🔍 SEARCH", "😇 MY PROFILE")
    markup.add("🤖 BOT CLONE", "🛠 SUPPORT")
    bot.send_message(
        user_id,
        "👋 𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐓𝐎 𝐑𝐔𝐃𝐎-𝐈𝐍𝐅𝐎 𝐁𝐎𝐓\nPlease choose an option below:",
        reply_markup=markup
    )

# =============================
# START COMMAND
# =============================
@bot.message_handler(commands=['start'])
def start(message):
    if is_muted(message.from_user.id):
        bot.reply_to(message, "⛔ You are muted for 1 day.")
        return

    force_join_check(message)

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

        bot.send_message(user_id, msg)
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
# BOT CLONE (Multi-threaded)
# =============================
def run_clone_bot(token):
    clone_bot = telebot.TeleBot(token)

    @clone_bot.message_handler(commands=['start'])
    def start_clone(message):
        clone_bot.reply_to(message, "👋 Clone Bot is running!")

    @clone_bot.message_handler(func=lambda m: True)
    def handle_message(message):
        clone_bot.reply_to(message, f"Echo: {message.text}")

    clone_bot.polling()

@bot.message_handler(func=lambda m: m.text == "🤖 BOT CLONE")
def bot_clone(message):
    bot.send_message(message.chat.id, "⚠️ Enter your bot token to clone features (Example: 1234:ABC-XYZ)")
    bot.register_next_step_handler(message, process_clone)

def process_clone(message):
    token = message.text.strip()
    username = message.from_user.username or "NoUsername"

    with open(CLONE_LOG, "a", encoding="utf-8") as f:
        f.write(f"{username} | {token} at {datetime.datetime.now()}\n")

    bot.reply_to(message, f"✅ Clone token saved for {username}")

    # Start clone bot in new thread
    threading.Thread(target=run_clone_bot, args=(token,), daemon=True).start()

# =============================
# SUPPORT
# =============================
@bot.message_handler(func=lambda m: m.text == "🛠 SUPPORT")
def support(message):
    bot.reply_to(message, "🛠 For support contact: @RUDOWNER")

# =============================
# ADMIN /CREDIT COMMAND
# =============================
@bot.message_handler(commands=['credit'])
def admin_credit(message):
    if message.from_user.id not in ADMIN_IDS:
        return
    try:
        _, amount, uid = message.text.split()
        update_credits(uid, int(amount), datetime.date.today().isoformat())
        bot.reply_to(message, f"Credits updated! {amount} points added to user {uid}.")
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {e}")

# =============================
# RUN MAIN BOT
# =============================
bot.polling()
