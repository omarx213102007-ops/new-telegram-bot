import asyncio
import time
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart

# ===== CONFIG =====
BOT_TOKEN = "8375264634:AAF5IjXO3pB_eMkFENii3LXtDwKwfNa987I"
ANTI_SPAM_TIME = 5

# ===== BOT =====
bot = Bot(BOT_TOKEN)
dp = Dispatcher()

user_last_message = {}

def is_spam(user_id: int):
    now = time.time()
    last = user_last_message.get(user_id, 0)
    if now - last < ANTI_SPAM_TIME:
        return True
    user_last_message[user_id] = now
    return False

# ===== START =====
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "✅ البوت شغال بدون أخطاء حالياً\n\n"
        "📌 احنا في مرحلة البرمجة\n"
        "أي رسالة منك معناها إن البوت شغال"
    )

# ===== TEXT =====
@dp.message(F.text)
async def any_text(message: Message):
    if is_spam(message.from_user.id):
        return
    await message.answer("🟢 تمام، البوت مستلم رسالتك")

# ===== RUN =====
async def main():
    print("Bot is running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
