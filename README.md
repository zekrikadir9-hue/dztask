# Telegram_Services_Bot - بوت الخدمات والرصيد (DZD)

بوت تيليجرام يوفر خدمات مشاهدة الفيديوهات وتصفح المواقع مقابل رصيد وهمي بالدينار الجزائري (DZD)، مع نظام سحب عند الوصول إلى حد معين.

## الخدمات المقدمة:
- مشاهدة الفيديوهات (50 د.ج)
- تصفح المواقع (30 د.ج)
- ألعاب صغيرة عن تاريخ الجزائر (20 د.ج)

## الميزات:
- **نظام الرصيد الوهمي:** تجميع الرصيد حتى 500 د.ج.
- **زر السحب:** إتاحة طلب السحب عند بلوغ 500 د.ج.
- **دعم العملاء:** تواصل عبر الإيميل (`kaderezakariaa@gmail.com`).

## 🛠️ متطلبات التشغيل

1. **Python 3.x**
2. **Git**
3. **التوكن:** رمز البوت الخاص بك من BotFather.

## 🚀 كيفية التشغيل

1. **استنساخ المستودع (Clone the repository):**
   ```bash
   git clone [رابط مستودعك على GitHub]
   cd Telegram_Services_Bot
   ```
2. **تثبيت المكتبات المطلوبة:**
   ```bash
   pip install -r requirements.txt
   ```
3. **تعيين التوكن كمتغير بيئة:**
   ```bash
   set TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN  # لنظام Windows
   export TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN  # لنظام Linux/Mac
   ```
4. **تشغيل البوت:**
   ```bash
   python bot.py
   ```