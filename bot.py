import telebot
from telebot.types import LabeledPrice

# Siz bergan Bot Token
API_TOKEN = '8537771100:AAFep8cQ3O_ev_DIrKmzcl0CRLdix1CWg2E'

# To'lovni test qilish uchun hozircha ixtiyoriy matn turibdi
PROVIDER_TOKEN = 'BU_YERGA_TEST_PAYMENT_TOKEN_QO_YING'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("💎 TikTok Tangalar sotib olish")
    bot.send_message(
        message.chat.id, 
        f"Salom! TikTok tangalari botiga xush kelibsiz!\nSizning Telegram ID: `{message.chat.id}`", 
        parse_mode="Markdown",
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: message.text == "💎 TikTok Tangalar sotib olish")
def show_coins(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text="⚡️ 50 Tanga - 15 000 so'm", callback_data="buy_50_coins"))
    bot.send_message(message.chat.id, "Kerakli tanga miqdorini tanlang:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "buy_50_coins")
def send_invoice(call):
    prices = [LabeledPrice(label='50 TikTok Coins', amount=1500000)]
    try:
        bot.send_invoice(
            call.message.chat.id,
            title="TikTok Tangalari",
            description="50 dona TikTok tangalari. To'lovdan so'ng hisobingizga tushadi.",
            provider_token=PROVIDER_TOKEN,
            currency='UZS',
            prices=prices,
            start_parameter='tiktok-coins-50',
            invoice_payload='payload_50_coins'
        )
    except Exception as e:
        bot.send_message(call.message.chat.id, "❌ To'lov tizimi hali to'liq sozlanmagan. PROVIDER_TOKEN kiritilishi kerak.")

@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True, error_message="To'lovda xatolik yuz berdi.")

@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    bot.send_message(message.chat.id, "🎉 To'lov muvaffaqiyatli amalga oshirildi! Iltimos, TikTok ID-ngizni yuboring.")

print("Bot muvaffaqiyatli ishga tushdi...")
bot.polling(none_stop=True)
