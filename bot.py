import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import os

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

user_balances = {} 

PRICES = {
    'watch_video': 50,  
    'browse_web': 30,   
    'play_games': 20    
}

MIN_WITHDRAWAL = 500

def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id not in user_balances:
        user_balances[user_id] = 0
    balance = user_balances[user_id]
    keyboard = [
        [InlineKeyboardButton("📺 مشاهدة الفيديوهات (50 د.ج)", callback_data='service_watch_video')],
        [InlineKeyboardButton("🌐 تصفح المواقع (30 د.ج)", callback_data='service_browse_web')],
        [InlineKeyboardButton("🎮 ألعاب وتاريخ الجزائر (20 د.ج)", callback_data='service_play_games')],
        [InlineKeyboardButton("💰 رصيدي/سحب", callback_data='show_balance')],
        [InlineKeyboardButton("✉️ دعم العملاء", callback_data='support_contact')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        f"مرحباً بك! رصيدك الحالي هو: **{balance} د.ج**.
اختر الخدمة التي تريدها:',
        reply_markup=reply_markup,
        parse_mode=telegram.ParseMode.MARKDOWN
    )

def handle_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    user_id = query.from_user.id
    data = query.data
    if data.startswith('service_'):
        service_key = data.split('_')[1]
        price = PRICES.get(service_key, 0)
        user_balances[user_id] += price
        new_balance = user_balances[user_id]
        message = f"✅ تم تفعيل الخدمة بنجاح!.
"
        if service_key == 'watch_video':
            message += f"تمت إضافة **{price} د.ج** إلى رصيدك. ابدأ مشاهدة الفيديو الآن."
        elif service_key == 'browse_web':
            message += f"تمت إضافة **{price} د.ج** إلى رصيدك. تفضل برابط تصفح المواقع."
        elif service_key == 'play_games':
            message += f"تمت إضافة **{price} د.ج** إلى رصيدك. إليك رابط الألعاب المصغرة."
        message += f"
رصيدك الجديد: **{new_balance} د.ج**."
        query.edit_message_text(message, parse_mode=telegram.ParseMode.MARKDOWN)
    elif data == 'show_balance':
        balance = user_balances.get(user_id, 0)
        keyboard = [[InlineKeyboardButton("🔄 العودة للقائمة", callback_data='return_to_menu')]]
        if balance >= MIN_WITHDRAWAL:
             keyboard.insert(0, [InlineKeyboardButton("💸 طلب سحب الرصيد", callback_data='request_withdrawal')])
             message = f"💰 رصيدك الحالي: **{balance} د.ج**.
تهانينا! يمكنك الآن طلب السحب."
        else:
             needed = MIN_WITHDRAWAL - balance
             message = f"💰 رصيدك الحالي: **{balance} د.ج**.
⚠️ الحد الأدنى للسحب هو {MIN_WITHDRAWAL} د.ج. ما زلت بحاجة إلى **{needed} د.ج**."
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(message, reply_markup=reply_markup, parse_mode=telegram.ParseMode.MARKDOWN)
    elif data == 'request_withdrawal':
        query.edit_message_text("✅ تم تسجيل طلب السحب! سيتم التواصل معك قريباً على حسابك في تيليجرام لإتمام عملية الدفع.")
    elif data == 'support_contact':
        support_email = "kaderezakariaa@gmail.com"
        message = f"📧 **دعم العملاء**:
إذا واجهتك أي مشكلة، يرجى إرسال رسالة إلينا عبر البريد الإلكتروني:
`{support_email}`
وسنقوم بالرد عليك في أقرب وقت ممكن. شكراً لك."
        keyboard = [[InlineKeyboardButton("🔄 العودة للقائمة", callback_data='return_to_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(message, reply_markup=reply_markup, parse_mode=telegram.ParseMode.MARKDOWN)
    elif data == 'return_to_menu':
        start(query, context)

def main() -> None:
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(handle_callback))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    print("البوت قيد التشغيل...")
    main()
