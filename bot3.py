from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, filters

# Thay token bot của bạn vào đây
TOKEN = "7337071978:AAFX4KYI49CbmYHbWAKdGoEMf0Za142BPKk"
# Thay link kênh thông báo của bạn vào đây
CHANNEL_LINK = "https://t.me/+MPYtI16HEBVmOTg1"
# Thay Telegram Admin
ADMIN_TELEGRAM = "https://t.me/minhvuzx"
# Link ảnh từ Imgur
IMAGE_URL = "https://imgur.com/02pfwuN.jpg"
IMAGE_1 = "https://imgur.com/epHJzUR.jpg"
IMAGE_2 = "https://imgur.com/uBeFSSj.jpg"
IMAGE_3 = "https://imgur.com/YRuqbJk.jpg"
IMAGE_LAST = "https://imgur.com/wlOW0JD"

async def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("KÊNH THÔNG BÁO🔔", url=CHANNEL_LINK)],
        [InlineKeyboardButton("✅ ĐÃ THAM GIA", callback_data="dathamgia")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = (f"Xin chào {update.message.from_user.first_name} 👋\n\n"
            "Vui lòng bấm vào nút **KÊNH THÔNG BÁO** và chọn **JOIN** hoặc **THAM GIA** kênh thông báo!!.\n\n"
            "🔔 **Bắt buộc phải đăng kí kênh** để nhận thông báo khi nào nhận lương!.\n\n"
            "Sau đó quay lại và bấm vào ✅ **ĐÃ THAM GIA**.")
    
    await update.message.reply_photo(photo=IMAGE_URL, caption=text, reply_markup=reply_markup, parse_mode="Markdown")

async def button_click(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == "dathamgia":
        keyboard = [
            [InlineKeyboardButton("📄BÀI LÀM", callback_data="bailam")],
            [InlineKeyboardButton("⏳TIME", callback_data="time")],
            [InlineKeyboardButton("⚠️ LƯU Ý ", callback_data="luuy")],
            [InlineKeyboardButton("👫MỜI VÀO NHÓM", callback_data="moivaonhom")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        message = ("Xin chào 👋\n\n"
                   "Bấm các nút phía dưới👇👇để được hướng dẫn.")
        await query.message.reply_text(message, reply_markup=reply_markup, parse_mode="Markdown")

    elif query.data == "bailam":
        message = ("<pre>Tuyển người vào nhóm rồi chụp màn hình lại nhận công (60k/1 lần).\n"
                   "Chỉ cần vào mời nhóm rồi chụp ảnh màn hình gửi mình là được.\n"
                   "IB Telegram:@minhvuzx có tích xanh</pre>\n\n"
                   "<b>Cách Sao Chép ⤴️⤴️</b>\n"
                   "Bạn bấm vào chữ bên trên, nội dung sẽ tự động sao chép.")
        
        keyboard = [[InlineKeyboardButton("ADMIN", url=ADMIN_TELEGRAM)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.message.reply_text(message, reply_markup=reply_markup, parse_mode="HTML")
        
        work_message = ("<b>Cách làm việc</b>\n"
                        "Bạn tham gia các nhóm trên Facebook 'Việc làm online, Tìm việc làm'....\n"
                        "Sau đó bạn đăng nội dung đó vào các hội nhóm rồi chụp lại gửi cho @minhvuzx.\n\n"
                        "* Đăng ít nhất 10 bài viết hoặc 30 bình luận mới có lương và không giới hạn số lần làm mỗi ngày.\n"
                                 "(1 bài đăng giá 10k).")
        
        await query.message.reply_text(work_message, parse_mode="HTML")
        await query.message.reply_photo(photo=IMAGE_1)
        await query.message.reply_photo(photo=IMAGE_2)
        await query.message.reply_photo(photo=IMAGE_3)
        await query.message.reply_photo(photo=IMAGE_LAST)
        await query.message.reply_text("Nếu bài đăng không được duyệt bạn có thể đi bình luận các bài viết, mỗi bài giá 5k.")

    elif query.data == "time":
        time_message = ("<b>Thời gian làm việc</b>\n"
                        "• 8h sáng bạn đi đăng trên fb rồi chụp lại (Rảnh lúc nào làm lúc đó).\n\n"
                        "• 12h bạn gửi những ảnh bạn đi đăng bài qua Telegram @minhvuzx.\n\n"
                        "• Nếu qua 12h bạn làm thêm thì gửi qua trước 19H.")
        await query.message.reply_text(time_message, parse_mode="HTML")

        salary_message = ("<b>Thời gian nhận lương</b>\n"
                          "• LƯƠNG SẼ ĐƯỢC NHẬN VÀO 19H-19H30.\n\n"
                          "• Khi nào kênh thông báo yêu cầu CTV gửi STK để nhận lương thì bạn vui lòng gửi STK qua cho @minhvuzx.")
        await query.message.reply_text(salary_message, parse_mode="HTML")

        example_message = ("<b>Ví dụ</b>\n"
                           "• Sáng 8h bạn làm được 17 cmt thì gửi qua mình lúc 12h trưa.\n\n"
                           "• Nếu sau 12h bạn làm thêm 22 cmt thì bạn gửi qua mình lúc nào cũng được, miễn trước 19h tối.")
        await query.message.reply_text(example_message, parse_mode="HTML")

        # Thêm 3 dấu chấm tách riêng biệt
        await query.message.reply_text(".")
        await query.message.reply_text(".")

    elif query.data == "luuy":
        note_message = ("⚠️ <b>Lưu Ý</b>\n\n"
                        "• Nếu FB bạn bị khóa comment hoặc đăng bài 24h thì có thể dùng acc FB khác làm.\n\n"
                        "• Bình luận trên 30 bài mới có lương và làm bao nhiêu nhận bấy nhiêu. "
                        "Trên 100 bài sẽ được thưởng thêm.\n\n"
                        "• Nếu đăng bài không được thì các CTV có thể đổi nhóm và tiếp tục làm như các bước hướng dẫn.\n\n"
                        "• Làm xong 12h trưa gửi ảnh qua cho chủ group: @minhvuzx.\n\n"
                        "• Bên mình chỉ có duy nhất @minhvuzx là chủ group và trợ lý bank, "
                        "không có ai mang danh cùng công ty để đi lừa mọi người. Nếu mất tiền mình không chịu trách nhiệm!!!")
        await query.message.reply_text(note_message, parse_mode="HTML")       

        # Thêm 3 dấu chấm tách riêng biệt
        await query.message.reply_text(".")
        await query.message.reply_text(".")

 
    elif query.data == "moivaonhom":
        invite_message = (
            "<b>Hướng dẫn mời vào nhóm:</b>\n\n"
            "• Bạn mời 1 người vào nhóm là được 60k.\n\n"
        )
        await query.message.reply_text(invite_message, parse_mode="HTML")

        step_1 = (
            "• Bạn bấm vào sao chép link nhóm ở dưới\n"
            "<code>https://t.me/+MPYtI16HEBVmOTg1</code>,\n"
       "  rồi mời người khác vào.\n\n"
        )
        await query.message.reply_text(step_1, parse_mode="HTML")

        step_2 = (
            "• Xong, bạn nhớ chụp lại tên Telegram của người đó và gửi cho @minhvuzx.\n\n"
        )
        await query.message.reply_text(step_2, parse_mode="HTML")

        step_3 = (
            "• Bạn mời họ vào nhóm,họ tham gia nhóm là được.\n\n"
        )
        await query.message.reply_text(step_3, parse_mode="HTML")

        step_4 = (
            "• Bạn mời người khác vào nhóm thì phải đăng ít nhất 10 bài viết mới được tính lượt mời."
        )
        await query.message.reply_text(step_4, parse_mode="HTML")

        # Thêm 3 dấu chấm tách riêng biệt
        await query.message.reply_text(".")
        await query.message.reply_text(".")


async def handle_message(update: Update, context: CallbackContext) -> None:
    # Phản hồi khi người dùng gửi tin nhắn hoặc ảnh
    response_message = (
        "Vui lòng không gửi ảnh, cmt hoặc nhắn tin cho bot hướng dẫn.\n\n"
        "Hãy vui lòng nhắn tin cho @minhvuzx để được hướng dẫn.\n\n"
        "Bấm ở đây để chạy lại Bot ➡️➡️/start"
    )
    await update.message.reply_text(response_message)

def main() -> None:
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_click))
    
    # Thêm handler để xử lý mọi tin nhắn và ảnh
    application.add_handler(MessageHandler(filters.TEXT | filters.PHOTO, handle_message))
    
    print("Bot đang chạy...")
    application.run_polling()

if __name__ == '__main__':
    main()
