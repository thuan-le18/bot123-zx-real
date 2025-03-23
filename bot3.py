import json
import os
import time
import logging
from functools import wraps
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, filters
from telegram.error import BadRequest

# Thay token bot của bạn vào đây
TOKEN = "7438193188:AAFUoblPvUvthTGAJS9YXCDh751-AhSxfKE"
# Thay link kênh thông báo của bạn vào đây (dùng cho nút bấm)
CHANNEL_LINK = "https://t.me/+MPYtI16HEBVmOTg1"
# Thay ID của kênh (hoặc nhóm) mà bạn muốn kiểm tra thành viên
CHANNEL_ID = -1002422341104 
# Thay Telegram Admin (dùng cho nút ADMIN và lệnh /unban)
ADMIN_TELEGRAM = "https://t.me/minhvuzx"
# Thay ADMIN_ID thành ID của admin (kiểu số)
ADMIN_ID = 1985817060

# Link ảnh từ Imgur
IMAGE_URL = "https://imgur.com/02pfwuN.jpg"
IMAGE_1 = "https://imgur.com/epHJzUR.jpg"
IMAGE_2 = "https://imgur.com/uBeFSSj.jpg"
IMAGE_3 = "https://imgur.com/YRuqbJk.jpg"
IMAGE_LAST = "https://imgur.com/wlOW0JD"

USERS_FILE = "users.json"
BOT_MESSAGES = {}

# ----------------- Quản lý file JSON -----------------
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def update_user_activity(user_id, chat_id=None):
    users = load_users()
    current_status = users.get(str(user_id), {}).get("banned", False)
    # Nếu có chat_id mới được cung cấp, lưu luôn; nếu không, giữ lại chat_id cũ (nếu có)
    old_chat = users.get(str(user_id), {}).get("chat_id", None)
    users[str(user_id)] = {"last_active": time.time(), "banned": current_status, "chat_id": chat_id or old_chat}
    save_users(users)

def is_banned(user_id):
    users = load_users()
    status = users.get(str(user_id), {}).get("banned", False)
    return status

# Tự động ban nếu không hoạt động quá 1 ngày và tự động xóa tin nhắn (nếu có chat_id)
async def auto_ban_job(context: CallbackContext):
    users = load_users()
    now = time.time()
    for user_id, data in users.items():
        # Nếu chưa bị ban và không hoạt động quá 1 ngày (1*24*3600 giây)
        if not data.get("banned", False) and now - data["last_active"] > 1 * 24 * 3600:
            users[user_id]["banned"] = True
            save_users(users)
            chat_id = data.get("chat_id")
            if chat_id:
                try:
                    await context.bot.send_message(chat_id=chat_id, text="You've been banned ")
                except Exception as e:
                await delete_bot_messages(user_id, chat_id, context)
# -----------------------------------------------------

# ----------------- Helper functions -----------------
def store_bot_message(user_id, message_id):
    BOT_MESSAGES.setdefault(str(user_id), []).append(message_id)

async def delete_bot_messages(user_id, chat_id, context: CallbackContext):
    message_ids = BOT_MESSAGES.get(str(user_id), [])
    for msg_id in message_ids:
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
        except Exception as e:
    BOT_MESSAGES[str(user_id)] = []

def check_banned(func):
    @wraps(func)
    async def wrapper(update: Update, context: CallbackContext):
        # Nếu là admin thì bỏ qua kiểm tra ban
        if update.message:
            user_id = update.message.from_user.id
            chat_id = update.message.chat.id
        elif update.callback_query:
            user_id = update.callback_query.from_user.id
            chat_id = update.callback_query.message.chat.id
        else:
            return await func(update, context)
        if user_id == ADMIN_ID:
            return await func(update, context)
        if is_banned(user_id):
            await context.bot.send_message(chat_id=chat_id, text="You've been banned")
            await delete_bot_messages(user_id, chat_id, context)
            return
        return await func(update, context)
    return wrapper
# -----------------------------------------------------

# ----------------- Handler của bot -----------------
@check_banned
async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    chat_id = update.message.chat.id
    update_user_activity(user_id)
    
    keyboard = [
        [InlineKeyboardButton("KÊNH THÔNG BÁO🔔", url=CHANNEL_LINK)],
        [InlineKeyboardButton("✅ ĐÃ THAM GIA", callback_data="dathamgia")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = (
        f"Xin chào {update.message.from_user.first_name} 👋\n\n"
        "Vui lòng bấm vào nút **KÊNH THÔNG BÁO** để tham gia kênh thông báo!\n\n"
        "Sau khi đã tham gia, bấm nút **✅ ĐÃ THAM GIA** để được hướng dẫn."
    )
    
    msg = await update.message.reply_photo(photo=IMAGE_URL, caption=text, reply_markup=reply_markup, parse_mode="Markdown")
    store_bot_message(user_id, msg.message_id)

@check_banned
async def button_click(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    chat_id = query.message.chat.id  # Lấy chat_id
    update_user_activity(user_id, chat_id)  # Lưu luôn chat_id
    
    if query.data == "dathamgia":
        try:
            member = await context.bot.get_chat_member(CHANNEL_ID, user_id)
        except BadRequest as e:
            if "user not found" in str(e).lower():
                await query.message.reply_text("Bạn cần tham gia nhóm trước!")
                return
            else:
                await query.message.reply_text("Không thể kiểm tra tham gia nhóm, vui lòng thử lại sau.")
                return

        if member.status not in ["member", "creator", "administrator"]:
            await query.message.reply_text("Bạn cần tham gia nhóm trước để có thể dùng bot!")
            return

        keyboard = [
            [InlineKeyboardButton("📄BÀI LÀM", callback_data="bailam")],
            [InlineKeyboardButton("⏳TIME", callback_data="time")],
            [InlineKeyboardButton("⚠️ LƯU Ý", callback_data="luuy")],
            [InlineKeyboardButton("👫MỜI VÀO NHÓM", callback_data="moivaonhom")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        msg = await query.message.reply_text("Xin chào 👋\n\nBạn Bấm vào các nút phía dưới👇👇để được hướng dẫn.", reply_markup=reply_markup, parse_mode="Markdown")
        store_bot_message(user_id, msg.message_id)

    elif query.data == "bailam":
        msg = await query.message.reply_text(
            "<pre>Tuyển người vô nhóm rồi chụp màn hình lại nhận công (60k 1 lần). "
            "Chỉ cần vô nhóm, chụp ảnh màn hình gửi mình là được. "
            "Ib telegram @minhvuzx có tích xanh.</pre>\n"
            "<b>Cách Sao Chép ⤴️⤴️</b>\n\n"
            "Bạn bấm vào chữ bên trên, nội dung sẽ tự động sao chép.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ADMIN", url=ADMIN_TELEGRAM)]]),
            parse_mode="HTML"
        )
        store_bot_message(user_id, msg.message_id)
        msg = await query.message.reply_text(
            "<b>Cách làm việc cho ctv</b>\n\n"
            "Bạn tham gia các nhóm trên Facebook 'Việc làm online, Tìm việc làm'...\n"
            "Sau đó bạn đăng nội dung vào các hội nhóm rồi chụp lại gửi cho @minhvuzx.\n\n"
            "* Đăng ít nhất 10 bài viết hoặc 30 bình luận mới có lương và không giới hạn số lần làm mỗi ngày.\n"
            "(1 bài đăng giá 10k).",
            parse_mode="HTML"
        )
        store_bot_message(user_id, msg.message_id)
        for photo in [IMAGE_1, IMAGE_2, IMAGE_3, IMAGE_LAST]:
            photo_msg = await query.message.reply_photo(photo=photo)
            store_bot_message(user_id, photo_msg.message_id)
        msg = await query.message.reply_text("Nếu bài đăng không được duyệt, bạn có thể đi bình luận các bài viết, mỗi bài giá 5k.")
        store_bot_message(user_id, msg.message_id)

    elif query.data == "time":
        msg = await query.message.reply_text(
            "<b>Thời gian làm việc cho ctv</b>\n"
            "8h sáng bạn đi đăng trên fb rồi chụp lại (Rảnh lúc nào làm lúc đó)\n\n"
            "12h bạn gửi những ảnh bạn đi đăng bài qua Telegram @minhvuzx.\n\n"
            "Nếu qua 12h bạn làm thêm thì gửi qua trước 19H.",
            parse_mode="HTML"
        )
        store_bot_message(user_id, msg.message_id)
        msg = await query.message.reply_text(
            "LƯƠNG SẼ ĐƯỢC NHẬN VÀO 19H-19H30.\n\n"
            "Khi nào kênh thông báo yêu cầu CTV gửi STK để nhận lương thì bạn vui lòng gửi STK qua cho @minhvuzx.",
            parse_mode="HTML"
        )
        store_bot_message(user_id, msg.message_id)
        msg = await query.message.reply_text(
            "<b>Ví dụ</b>\n"
            "Sáng 8h bạn làm được 17 cmt thì gửi qua mình lúc 12h trưa.\n\n"
            "Nếu sau 12h bạn làm thêm 22 cmt thì bạn gửi qua mình lúc nào cũng được, miễn trước 19h tối.",
            parse_mode="HTML"
        )
        store_bot_message(user_id, msg.message_id)
        msg = await query.message.reply_text(".")
        store_bot_message(user_id, msg.message_id)
        msg = await query.message.reply_text(".")
        store_bot_message(user_id, msg.message_id)

    elif query.data == "luuy":
        msg = await query.message.reply_text(
            "⚠️ <b>Lưu Ý</b>\n\n"
            "• Nếu FB của bạn bị khóa comment hoặc đăng bài 24h thì có thể dùng acc FB khác làm.\n\n"
            "• Bình luận trên 30 bài mới có lương và làm bao nhiêu nhận bấy nhiêu. Trên 100 bài sẽ được thưởng thêm.\n\n"
            "• Nếu đăng bài không được thì các CTV có thể đổi nhóm và tiếp tục làm như các bước hướng dẫn.\n\n"
            "• Làm xong 12h trưa gửi ảnh qua cho chủ group: @minhvuzx.\n\n"
            "• Chỉ có @minhvuzx là chủ group và trợ lý bank, không ai mang danh cùng công ty để đi lừa mọi người. Nếu mất tiền mình không chịu trách nhiệm!!!",
            parse_mode="HTML"
        )
        store_bot_message(user_id, msg.message_id)
        msg = await query.message.reply_text(".")
        store_bot_message(user_id, msg.message_id)
        msg = await query.message.reply_text(".")
        store_bot_message(user_id, msg.message_id)

    elif query.data == "moivaonhom":
        msg = await query.message.reply_text("Bạn mời 1 người vào nhóm là được 60k.\n\n", parse_mode="HTML")
        store_bot_message(user_id, msg.message_id)
        msg = await query.message.reply_text(
            "Bạn bấm sao chép link nhóm ở dưới lại rồi mời người khác vào.\n"
            "<code>https://t.me/+MPYtI16HEBVmOTg1</code>\n",
            parse_mode="HTML"
        )
        store_bot_message(user_id, msg.message_id)
        msg = await query.message.reply_text(
            "Bạn mời họ vào nhóm, họ tham gia nhóm là được. Xong, bạn nhớ chụp lại tên Telegram của người đó và gửi cho @minhvuzx\n",
            parse_mode="HTML"
        )
        store_bot_message(user_id, msg.message_id)
        msg = await query.message.reply_text(
            "Bạn mời người khác vào nhóm thì đi đăng ít nhất 10 bài viết mới được tính lượt mời.",
            parse_mode="HTML"
        )
        store_bot_message(user_id, msg.message_id)
        msg = await query.message.reply_text(".")
        store_bot_message(user_id, msg.message_id)
        msg = await query.message.reply_text(".")
        store_bot_message(user_id, msg.message_id)

@check_banned
async def handle_message(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    chat_id = update.message.chat.id
    update_user_activity(user_id)
    msg = await update.message.reply_text(
        "Vui lòng không gửi ảnh, cmt hoặc nhắn tin cho bot hướng dẫn.\n\n"
        "Hãy nhắn tin cho @minhvuzx để được hướng dẫn.\n\n"
        "Bấm ở đây để chạy lại Bot ➡️➡️/start"
    )
    store_bot_message(user_id, msg.message_id)

# Lệnh /ban cho Admin (không kiểm tra banned)
@check_banned  # Không cần decorator cho lệnh admin, nhưng nếu bạn muốn thì có thể bỏ qua
async def ban(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("Bạn không có quyền dùng lệnh này.")
        return
    if not context.args:
        await update.message.reply_text("Vui lòng cung cấp user_id cần ban, ví dụ: /ban 987654321")
        return
    target_id = str(context.args[0])
    logging.info("Admin banning user: %s", target_id)
    users = load_users()
    # Cập nhật trạng thái ban
    users[target_id] = {"last_active": time.time(), "banned": True, "chat_id": users.get(target_id, {}).get("chat_id")}
    save_users(users)
    await update.message.reply_text(f"Đã ban người dùng {target_id}")
    
    # Nếu user đã có chat_id lưu, xóa luôn các tin nhắn của bot
    target_data = users.get(target_id, {})
    chat_id = target_data.get("chat_id")
    if chat_id:
        # Gọi hàm xóa tin nhắn ngay
        await delete_bot_messages(target_id, chat_id, context)

# Lệnh /unban cho Admin (không kiểm tra banned)
@check_banned
async def unban(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("Bạn không có quyền dùng lệnh này.")
        return
    if not context.args:
        await update.message.reply_text("Vui lòng cung cấp user_id cần gỡ ban, ví dụ: /unban 987654321")
        return
    target_id = str(context.args[0])
    users = load_users()
    if target_id in users:
        users[target_id]["banned"] = False
        save_users(users)
        await update.message.reply_text(f"Đã gỡ ban người dùng {target_id}")
    else:
        await update.message.reply_text("Không tìm thấy người dùng trong danh sách.")

def main() -> None:
    # Lên lịch tự động ban sau 1 ngày không hoạt động
    async def job_auto_ban(context: CallbackContext):
        users = load_users()
        now = time.time()
        for user_id, data in users.items():
            if not data.get("banned", False) and now - data["last_active"] > 1 * 24 * 3600:
                users[user_id]["banned"] = True
                save_users(users)
                chat_id = data.get("chat_id")
                if chat_id:
                    try:
                        await context.bot.send_message(chat_id=chat_id, text="You've been banned ")
                    except Exception as e:
                    await delete_bot_messages(user_id, chat_id, context)
    
    
    application = Application.builder().token(TOKEN).build()
    
    # Lên lịch job tự động chạy mỗi 60 giây
    job_queue = application.job_queue
    job_queue.run_repeating(job_auto_ban, interval=60, first=10)
    
    application.add_handler(CommandHandler("start", start), group=0)
    application.add_handler(CommandHandler("ban", ban), group=0)
    application.add_handler(CommandHandler("unban", unban), group=0)
    application.add_handler(CallbackQueryHandler(button_click), group=1)
    application.add_handler(MessageHandler((filters.TEXT & ~filters.COMMAND) | filters.PHOTO, handle_message), group=2)
    
    print("Bot hướng dẫn đang chạy...")
    application.run_polling()

if __name__ == '__main__':
    main()
