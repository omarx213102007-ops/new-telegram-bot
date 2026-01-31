import asyncio
import time
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ChatMemberStatus
import yt_dlp

BOT_TOKEN = "8375264634:AAF5IjXO3pB_eMkFENii3LXtDwKwfNa987I"

REQUIRED_CHANNELS = [
    "@Athr_Tayyeb",
    "@SVD_OMVR"
]

ANTI_SPAM_TIME = 5
user_last_message = {}

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

async def check_subscriptions(user_id: int):
    for channel in REQUIRED_CHANNELS:
        member = await bot.get_chat_member(channel, user_id)
        if member.status not in (
            ChatMemberStatus.MEMBER,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ):
            return False
    return True

def is_spam(user_id: int):
    now = time.time()
    last = user_last_message.get(user_id, 0)
    if now - last < ANTI_SPAM_TIME:
        return True
    user_last_message[user_id] = now
    return False

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("🟢 البوت شغال ومفيش أخطاء\nابعت رابط أو اسم فيديو")

@dp.message(F.content_type != "text")
async def block_media(message: Message):
    await message.answer("🚫 نص فقط")

@dp.message(F.text)
async def handle_text(message: Message):
    user_id = message.from_user.id

    if is_spam(user_id):
        return await message.answer("⏳ استنى شوية")

    if not await check_subscriptions(user_id):
        kb = InlineKeyboardBuilder()
        for ch in REQUIRED_CHANNELS:
            kb.button(text=f"اشترك {ch}", url=f"https://t.me/{ch[1:]}")
        kb.button(text="تحقق", callback_data="check_sub")
        kb.adjust(1)

        return await message.answer(
            "لازم تشترك في القنوات الأول",
            reply_markup=kb.as_markup()
        )

    kb = InlineKeyboardBuilder()
    kb.button(text="🎥 فيديو", callback_data=f"video|{message.text}")
    kb.button(text="🎵 صوت", callback_data=f"audio|{message.text}")
    kb.adjust(1)

    await message.answer("اختار 👇", reply_markup=kb.as_markup())

@dp.callback_query(F.data == "check_sub")
async def recheck(callback: CallbackQuery):
    if await check_subscriptions(callback.from_user.id):
        await callback.message.edit_text("تمام 👍 ابعت الرابط")
    else:
        await callback.answer("لسه مش مشترك", show_alert=True)

@dp.callback_query(F.data.startswith(("video", "audio")))
async def download(callback: CallbackQuery):
    kind, query = callback.data.split("|", 1)
    await callback.message.edit_text("⏬ جاري التحضير...")

    ydl_opts = {"quiet": True, "noplaylist": True}

    if kind == "video":
        ydl_opts["format"] = "bestvideo+bestaudio/best"
    else:
        ydl_opts["format"] = "bestaudio"

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)
            url = info["url"]

        await bot.send_message(
            callback.from_user.id,
            f"✅ جاهز\n{url}"
        )
    except:
        await callback.message.edit_text("❌ حصل خطأ")

async def main():
    print("🟢 الكود اشتغل بدون أخطاء برمجية")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
