import requests
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8838463638:AAFrdujcD3JdoPH_sTUvnk2pf-ogfoEjn-k"
GROQ_KEY = "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"
ADMIN_ID = 0

def ask_groq(text):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    data = {"model": "openai/gpt-oss-20b","messages": [{"role": "system", "content": "انت مساعد يمني بلهجة عدنية"},{"role": "user", "content": text}]}
    r = requests.post(url, headers=headers, json=data, timeout=30)
    return r.json()['choices'][0]['message']['content']

async def start(update, context):
    global ADMIN_ID
    if ADMIN_ID == 0:
        ADMIN_ID = update.message.from_user.id
        await update.message.reply_text(f"✅ انت الحين المالك\nايديك: {ADMIN_ID}\nاي حد يكلم البوت برسلك على الخاص", reply_markup=ReplyKeyboardRemove())
        return
    await update.message.reply_text("هلا! اسألني ✅", reply_markup=ReplyKeyboardRemove())

async def reply(update, context):
    global ADMIN_ID
    user = update.message.from_user
    text = update.message.text
    if ADMIN_ID == 0:
        ADMIN_ID = user.id
        return

    # يرسل لك على تليجرامك
    if user.id != ADMIN_ID:
        try:
            await context.bot.send_message(chat_id=ADMIN_ID, text=f"👤 واحد كلم بوتك:\nالاسم: {user.first_name}\nاليوزر: @{user.username}\nالايدي: {user.id}\n\nرسالته: {text}")
        except: pass

    ans = ask_groq(text)
    await update.message.reply_text(ans, reply_markup=ReplyKeyboardRemove())

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))
print("شغال - ارسل /start في تليجرام انت اول واحد")
app.run_polling()
