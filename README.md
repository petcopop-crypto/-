# Telegram Chat Bot + AI

هذا البوت يعمل بطريقتين:
1. غرفة دردشة بين المستخدمين (عبر أوامر /join و /leave).
2. أسئلة للذكاء الاصطناعي عبر الأمر /ai.

## الأوامر
- /join : الانضمام لغرفة الدردشة
- /leave : الخروج
- /users : عرض قائمة الأعضاء
- /ai <سؤال> : سؤال للذكاء الاصطناعي
- /help : تعليمات

## التشغيل على Render
1. أنشئ Repository جديد على GitHub وارفع الملفات.
2. اربط الريبو بـ Render كـ Worker.
3. أضف متغيرات البيئة:
   - BOT_TOKEN = التوكن من BotFather
   - OPENAI_API_KEY = مفتاح OpenAI API
4. اضغط Deploy.
