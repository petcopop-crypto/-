    import os
    import telebot
    import openai

    TOKEN = os.environ.get('BOT_TOKEN')
    OPENAI_KEY = os.environ.get('OPENAI_API_KEY')

    if not TOKEN:
        raise RuntimeError('Please set BOT_TOKEN environment variable (from BotFather).')
    if not OPENAI_KEY:
        raise RuntimeError('Please set OPENAI_API_KEY environment variable (from OpenAI).')

    bot = telebot.TeleBot(TOKEN)
    openai.api_key = OPENAI_KEY

    joined = {}

    HELP_TEXT = (
        "🤖 أوامر البوت:
"
        "/join - الانضمام إلى غرفة الدردشة
"
        "/leave - الخروج من الغرفة
"
        "/users - عرض الأعضاء
"
        "/ai <سؤال> - اسأل الذكاء الاصطناعي
"
        "/help - عرض هذه القائمة"
    )

    @bot.message_handler(commands=['start','help'])
    def send_help(message):
        bot.reply_to(message, HELP_TEXT)

    @bot.message_handler(commands=['join'])
    def join_chat(message):
        user_id = message.from_user.id
        name = message.from_user.first_name or ''
        if message.from_user.last_name:
            name += ' ' + message.from_user.last_name
        joined[user_id] = name.strip() or f'user_{user_id}'
        bot.reply_to(message, f"✅ انضممت لغرفة الدردشة. الآن رسائلك الخاصة ستُرسل لباقي الأعضاء ({len(joined)-1} آخرون).")

    @bot.message_handler(commands=['leave'])
    def leave_chat(message):
        user_id = message.from_user.id
        if user_id in joined:
            joined.pop(user_id)
            bot.reply_to(message, "✅ خرجت من غرفة الدردشة.")
        else:
            bot.reply_to(message, "أنت لست منضمًا للغرفة.")

    @bot.message_handler(commands=['users'])
    def list_users(message):
        if not joined:
            bot.reply_to(message, "لا يوجد أعضاء حاليًا في الغرفة.")
            return
        lines = [f"- {n}" for n in joined.values()]
        bot.reply_to(message, "أعضاء الغرفة:\n" + "\n".join(lines))

    @bot.message_handler(commands=['ai'])
    def ask_ai(message):
        query = message.text.replace('/ai', '', 1).strip()
        if not query:
            bot.reply_to(message, "✍️ اكتب سؤالك بعد الأمر /ai")
            return
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": query}],
                max_tokens=300,
                temperature=0.7
            )
            answer = response['choices'][0]['message']['content']
            bot.reply_to(message, f"🤖 {answer}")
        except Exception as e:
            bot.reply_to(message, f"❌ حصل خطأ: {e}")

    # Private message broadcast (chat room)
    @bot.message_handler(func=lambda m: m.chat.type == 'private' and m.text is not None and not m.text.startswith('/'))
    def private_message_handler(message):
        sender_id = message.from_user.id
        sender_name = (message.from_user.first_name or '') + ((' ' + message.from_user.last_name) if message.from_user.last_name else '')
        sender_name = sender_name.strip() or f'user_{sender_id}'

        if sender_id not in joined:
            bot.reply_to(message, "أنت لست مشتركًا في غرفة الدردشة. اكتب /join للانضمام.")
            return

        text = message.text
        recipients = [uid for uid in joined.keys() if uid != sender_id]
        if not recipients:
            bot.reply_to(message, "لا يوجد أعضاء آخرون في الغرفة حالياً.")
            return

        sent = 0
        for uid in recipients:
            try:
                bot.send_message(uid, f"📨 رسالة من {sender_name}:\n\n{text}")
                sent += 1
            except:
                pass
        bot.reply_to(message, f"تم إرسال رسالتك إلى {sent} عضو/أعضاء.")

    if __name__ == '__main__':
        print('Bot polling started...')
        bot.infinity_polling()
