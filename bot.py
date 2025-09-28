import telegram
import os
# تم تعديل الاستيراد ليتوافق مع الإصدارات الحديثة (v20+)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext
# هذا الاستيراد هو الحل لخطأ AttributeError: 'telegram' has no attribute 'ParseMode'
from telegram.constants import ParseMode

# 1. التكوين (Configuration)
# يُفضل جلب التوكن من متغيرات البيئة لضمان الأمان
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") 
SUPPORT_EMAIL = "kaderezakariaa@gmail.com"

# 2. قاعدة بيانات الأرصدة (مؤقتة - يرجى استبدالها بقاعدة بيانات دائمة عند النشر)
# الصيغة: user_id: balance_in_dzd
user_balances = {} 

# 3. الأسعار والحدود
PRICES = {
    'watch_video': 50,  # مشاهدة الفيديوهات (50 د.ج)
    'browse_web': 30,   # تصفح المواقع (30 د.ج)
    'play_games': 20    # الألعاب الصغيرة والتاريخ (20 د.ج)
}
MIN_WITHDRAWAL = 500

# ----------------- الدوال الأساسية -----------------

def start(update: Update, context: CallbackContext) -> None:
    """معالج أمر /start: الترحيب وعرض القائمة الرئيسية."""
    # نستخدم update.effective_chat إذا كانت الدالة تُستدعى من callback
    chat = update.message if update.message else update.callback_query.message
    user_id = chat.from_user.id
    
    if user_id not in user_balances:
        user_balances[user_id] = 0
        
    balance = user_balances[user_id]
    
    # بناء أزرار القائمة الرئيسية
    keyboard = [
        [InlineKeyboardButton("📺 مشاهدة الفيديوهات (50 د.ج)", callback_data='service_watch_video')],
        [InlineKeyboardButton("🌐 تصفح المواقع (30 د.ج)", callback_data='service_browse_web')],
        [InlineKeyboardButton("🎮 ألعاب وتاريخ الجزائر (20 د.ج)", callback_data='service_play_games')],
        [InlineKeyboardButton("💰 رصيدي/سحب", callback_data='show_balance')],
        [InlineKeyboardButton("✉️ دعم العملاء", callback_data='support_contact')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message_text = f"مرحباً بك! رصيدك الحالي هو: **{balance} د.ج**.\nاختر الخدمة التي تريدها:"
    
    chat.reply_text(
        message_text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN # استخدام ParseMode مباشرة بعد الاستيراد
    )

def handle_callback(update: Update, context: CallbackContext) -> None:
    """معالج النقر على الأزرار المضمنة (Inline Buttons)."""
    query = update.callback_query
    query.answer()
    
    user_id = query.from_user.id
    data = query.data
    
    # ----------------- 1. منطق الخدمات وزيادة الرصيد -----------------
    if data.startswith('service_'):
        service_key = data.split('_')[1]
        price = PRICES.get(service_key, 0)
        
        user_balances[user_id] = user_balances.get(user_id, 0) + price
        new_balance = user_balances[user_id]
        
        message = f"✅ تم تفعيل الخدمة بنجاح!.\n"
        
        if service_key == 'watch_video':
            message += f"تمت إضافة **{price} د.ج** إلى رصيدك. ابدأ مشاهدة الفيديو الآن."
        elif service_key == 'browse_web':
            message += f"تمت إضافة **{price} د.ج** إلى رصيدك. تفضل برابط تصفح المواقع."
        elif service_key == 'play_games':
            message += f"تمت إضافة **{price} د.ج** إلى رصيدك. إليك رابط الألعاب المصغرة."
            
        message += f"\nرصيدك الجديد: **{new_balance} د.ج**."
        query.edit_message_text(message, parse_mode=ParseMode.MARKDOWN) # تم التعديل هنا

    # ----------------- 2. منطق عرض الرصيد والسحب -----------------
    elif data == 'show_balance':
        balance = user_balances.get(user_id, 0)
        
        keyboard = [[InlineKeyboardButton("🔄 العودة للقائمة", callback_data='return_to_menu')]]
        
        if balance >= MIN_WITHDRAWAL:
             keyboard.insert(0, [InlineKeyboardButton("💸 طلب سحب الرصيد", callback_data='request_withdrawal')])
             message = f"💰 رصيدك الحالي: **{balance} د.ج**.\nتهانينا! يمكنك الآن طلب السحب."
        else:
             needed = MIN_WITHDRAWAL - balance
             message = f"💰 رصيدك الحالي: **{balance} د.ج**.\n⚠️ الحد الأدنى للسحب هو {MIN_WITHDRAWAL} د.ج. ما زلت بحاجة إلى **{needed} د.ج**."

        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(message, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN) # تم التعديل هنا

    elif data == 'request_withdrawal':
        query.edit_message_text(
            "✅ تم تسجيل طلب السحب! سيتم التواصل معك قريباً على حسابك في تيليجرام لإتمام عملية الدفع."
        )

    # ----------------- 3. منطق دعم العملاء والعودة -----------------
    elif data == 'support_contact':
        message = (
            f"📧 **دعم العملاء**:\n"
            f"إذا واجهتك أي مشكلة، يرجى إرسال رسالة إلينا عبر البريد الإلكتروني:\n"
            f"`{SUPPORT_EMAIL}`\n"
            f"وسنقوم بالرد عليك في أقرب وقت ممكن. شكراً لك."
        )
        
        keyboard = [[InlineKeyboardButton("🔄 العودة للقائمة", callback_data='return_to_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(message, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN) # تم التعديل هنا

    elif data == 'return_to_menu':
        # إعادة توجيه إلى دالة start لإعادة عرض القائمة
        # يجب أن نستخدم edit_message_text هنا لتجنب خطأ
        # "Message must be modified"
        # لكن سنستخدم start مباشرة ونعدل كيفية استدعائها.
        # نستخدم دالة edit_message_text لتبديل القائمة القديمة بالقائمة الجديدة
        
        # استدعاء دالة start لتبني الرسالة الجديدة
        # نستخدم update.callback_query بدلاً من update.message في start ليكون الاستدعاء متوافقاً
        
        user_id = query.from_user.id
        balance = user_balances.get(user_id, 0)
        
        keyboard = [
            [InlineKeyboardButton("📺 مشاهدة الفيديوهات (50 د.ج)", callback_data='service_watch_video')],
            [InlineKeyboardButton("🌐 تصفح المواقع (30 د.ج)", callback_data='service_browse_web')],
            [InlineKeyboardButton("🎮 ألعاب وتاريخ الجزائر (20 د.ج)", callback_data='service_play_games')],
            [InlineKeyboardButton("💰 رصيدي/سحب", callback_data='show_balance')],
            [InlineKeyboardButton("✉️ دعم العملاء", callback_data='support_contact')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        message_text = f"مرحباً بك! رصيدك الحالي هو: **{balance} د.ج**.\nاختر الخدمة التي تريدها:"

        query.edit_message_text(
            message_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )


# ----------------- دالة التشغيل الرئيسية -----------------

def main() -> None:
    """تشغيل البوت باستخدام الصيغة الحديثة لمكتبة python-telegram-bot (الإصدار 20+)."""
    
    if not TOKEN:
        print("خطأ فادح: لم يتم العثور على توكن البوت في متغيرات البيئة.")
        return

    # استخدام Application.builder() هي الطريقة الصحيحة للتشغيل الحديثة
    application = Application.builder().token(TOKEN).build()

    # ربط المعالجات بالأوامر والأزرار
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_callback))

    # بدء عملية استطلاع الرسائل (Polling) بشكل مستمر
    print("البوت جاهز. بدء الاستطلاع...")
    application.run_polling(poll_interval=3) 

if __name__ == '__main__':
    main()
