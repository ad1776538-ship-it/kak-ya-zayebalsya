import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
from telegram.constants import ChatAction
from mistralai import Mistral

TOKEN = os.getenv("8699789330:AAErx6x530YblxPi9x_tRRhDFsZ8b6s0Wvc")
MISTRAL_KEY = os.getenv("exhmzbfqfObMXGzRWnoegszu17lseJfM")

client = Mistral(api_key=MISTRAL_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я ЛядовGPT. Спрашивай!")

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text

    await update.message.chat.send_action(ChatAction.TYPING)

    try:
        response = client.chat.complete(
            model="mistral-small-latest",
            messages=[
                {"role": "system", "content": "Ты ЛядовGPT. Отвечай как человек. На русском."},
                {"role": "user", "content": msg}
            ]
        )

        await update.message.reply_text(response.choices[0].message.content)

    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

print("OK")
app.run_polling()