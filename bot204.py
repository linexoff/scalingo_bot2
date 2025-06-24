import json
import os
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    MessageHandler, ContextTypes, filters
)

BOT_TOKEN = "7442669013:AAH3EateroGENdEFznRfl9zviNK5d7LGGaA"
ADMIN_ID = 7864781525  # Замени на свой Telegram ID

DATA_FILE = "subscriptions.json"

def load_subscriptions():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_subscriptions(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

subscriptions = load_subscriptions()

# --- Команды ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = ReplyKeyboardMarkup(
        [[KeyboardButton("📋 Тарифы"), KeyboardButton("🛡 Ваша подписка")]],
        resize_keyboard=True
    )
    await update.message.reply_text(
        "👋 Привет! Добро пожаловать в Galaxy Бот.\n\nВыберите действие:",
        reply_markup=keyboard
    )

# --- Обработка текстовых кнопок меню ---

async def handle_text_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "📋 Тарифы":
        keyboard = [
            [InlineKeyboardButton("⭐️ Galaxy club — 499₽", callback_data="galaxy")],
            [InlineKeyboardButton("💖 Донат", callback_data="donate")],
            [InlineKeyboardButton("⬅️ Назад", callback_data="back_to_main")]
        ]
        await update.message.reply_text("📋 Выберите тариф:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif text == "🛡 Ваша подписка":
        user_id = update.message.from_user.id
        sub = subscriptions.get(str(user_id))
        if sub == "galaxy":
            await update.message.reply_text(
                "✅ Ваша подписка: Galaxy ⭐️ 𝒄𝒍𝒖𝒃\n\n🔗 [Перейти в канал](https://t.me/+Rz2eXtJY94pkYTMy)",
                parse_mode="Markdown"
            )
        else:
            await update.message.reply_text(
                "❌ У вас нет активных подписок. Перейти к покупке?",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("Оформить подписку", callback_data="tariffs")]]
                )
            )

# --- Кнопки ---

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    try:
        if query.data == "tariffs":
            keyboard = [
                [InlineKeyboardButton("⭐️ Galaxy club — 499₽", callback_data="galaxy")],
                [InlineKeyboardButton("💖 Донат", callback_data="donate")],
                [InlineKeyboardButton("⬅️ Назад", callback_data="back_to_main")]
            ]
            if query.message.text:
                await query.edit_message_text("📋 Выберите тариф:", reply_markup=InlineKeyboardMarkup(keyboard))
            else:
                await query.message.reply_text("📋 Выберите тариф:", reply_markup=InlineKeyboardMarkup(keyboard))

        elif query.data == "back_to_main":
            if query.message.text:
                await query.edit_message_text("↩️ Возвращено в главное меню. Выберите действие с клавиатуры снизу.")
            else:
                await query.message.reply_text("↩️ Возвращено в главное меню. Выберите действие с клавиатуры снизу.")

        elif query.data == "galaxy":
            text = (
                "🌟 *Galaxy ⭐️ 𝒄𝒍𝒖𝒃 (𝑽𝑰𝑷)* — 499₽\n\n"
                "*Описание Galaxy ⭐️ 𝒄𝒍𝒖𝒃 (𝑽𝑰𝑷):*\n"
                "Выдается за донат в 499₽.\n\n"
                "В нем вы найдете:\n"
                "• Продолжения ко всем постам с основного канала\n"
                "• Ежедневное пополнение контентом! *Над качеством артов для Вип канала я работаю значительно дольше. Вам понравится!*\n"
                "• Выбор следующих персонажей для основы и випки, а так же ваши предложения!\n\n"
                "По всем вопросам и предложениям - @galql"
            )
            keyboard = [
                [InlineKeyboardButton("💸 Оплатить", callback_data="pay_galaxy")],
                [InlineKeyboardButton("⬅️ Назад", callback_data="tariffs")]
            ]
            if query.message.text:
                await query.edit_message_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))
            else:
                await query.message.reply_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

        elif query.data == "donate":
            text = (
                "💖 *Донат*\n\n"
                "Спасибо за поддержку! Вы не получите доступ к контенту,\n"
                "но получите мою огромную благодарность ❤️\n\n"
                "Ваш вклад помогает проекту развиваться.\n\n"
                "Реквизиты:\nТ-Банк: 5536 9141 5550 3182\nАльфа Банк: 2200 1523 7703 6275\nКомментарий: Donat\n\n"
                "После оплаты нажмите «Я оплатил»"
            )
            keyboard = [
                [InlineKeyboardButton("✅ Я оплатил", callback_data="paid_donate")],
                [InlineKeyboardButton("⬅️ Назад", callback_data="tariffs")]
            ]
            if query.message.text:
                await query.edit_message_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))
            else:
                await query.message.reply_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

        elif query.data == "pay_galaxy":
            text = (
                "💳 Реквизиты:\n\n"
                "Т-Банк: 5536 9141 5550 3182\n"
                "Альфа Банк: 2200 1523 7703 6275\n"
                "Комментарий: GalaxyVIP\n\n"
                "После оплаты нажмите «Я оплатил» или нажмите «Отмена» чтобы вернуться."
            )
            keyboard = [
                [
                    InlineKeyboardButton("✅ Я оплатил", callback_data="paid_galaxy"),
                    InlineKeyboardButton("⬅️ Отмена", callback_data="tariffs")
                ]
            ]
            if query.message.text:
                await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
            else:
                await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

        elif query.data == "paid_galaxy":
            context.user_data["awaiting_screenshot"] = "galaxy"
            if query.message.text:
                await query.edit_message_text("📸 Пожалуйста, отправьте чек/скриншот оплаты в виде изображения.")
            else:
                await query.message.reply_text("📸 Пожалуйста, отправьте чек/скриншот оплаты в виде изображения.")

        elif query.data == "paid_donate":
            if query.message.text:
                await query.edit_message_text("💖 Спасибо за поддержку! Ваш донат важен для меня ❤️")
            else:
                await query.message.reply_text("💖 Спасибо за поддержку! Ваш донат важен для меня ❤️")

        elif query.data.startswith("confirm_galaxy_"):
            target_user_id = query.data.split("_")[-1]
            subscriptions[str(target_user_id)] = "galaxy"
            save_subscriptions(subscriptions)
            if query.message.text:
                await query.edit_message_text("✅ Подписка Galaxy успешно выдана!")
            else:
                await query.message.reply_text("✅ Подписка Galaxy успешно выдана!")

            # Уведомление пользователю
            try:
                await context.bot.send_message(
                    chat_id=int(target_user_id),
                    text="🎉 Ваша подписка Galaxy активирована!\n[Перейти в канал](https://t.me/+Rz2eXtJY94pkYTMy)",
                    parse_mode="Markdown"
                )
            except:
                pass

            # Уведомление админу
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=f"✅ Подписка Galaxy успешно выдана пользователю @{query.from_user.username} (ID: {target_user_id})"
            )

        elif query.data.startswith("cancel_"):
            if query.message.text:
                await query.edit_message_text("❌ Запрос отклонён.")
            else:
                await query.message.reply_text("❌ Запрос отклонён.")

            # Уведомление пользователю
            try:
                await context.bot.send_message(
                    chat_id=int(user_id),
                    text="❌ Ваш запрос на подписку был отклонён. Вы можете повторно оформить заявку."
                )
            except:
                pass

            # Уведомление админу
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=f"❌ Запрос на подписку пользователя @{query.from_user.username} (ID: {user_id}) был отклонён."
            )

    except Exception as e:
        # Логирование ошибки или выполнение другого действия в случае исключения
        print(f"Ошибка при редактировании сообщения: {e}")
        # Вы можете отправить новое сообщение, если редактирование не удаётся
        await query.message.reply_text("Произошла ошибка при попытке редактировать сообщение.")

# --- Фото: скриншот оплаты ---

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = user.id
    username = user.username or user.first_name
    tariff = context.user_data.get("awaiting_screenshot")

    if tariff == "galaxy":
        keyboard = [
            [
                InlineKeyboardButton("✅ Выдать Galaxy", callback_data=f"confirm_galaxy_{user_id}"),
                InlineKeyboardButton("❌ Отменить", callback_data=f"cancel_{user_id}")
            ]
        ]
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"📥 Скриншот оплаты от @{username} (ID: {user_id})"
        )
        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=update.message.photo[-1].file_id,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

        await update.message.reply_text(
            "Спасибо! Скриншот отправлен на проверку. Ожидайте подтверждения.\n\n"
            "❗ **ВАЖНО: НЕ ПОВТОРЯЙТЕ ОТПРАВКУ ЧЕКА ПО ОДНОЙ И ТОЙ ЖЕ ОПЛАТЕ!**\n\n"
            "Если с момента оплаты прошло более 24 часов — **НЕ НУЖНО повторно отправлять чек или скриншот!** "
            "Просто **напишите мне в личные сообщения — @galql.**\n\n"
            "✅ Если вы случайно вместо чека отправили скрин оплаты — не волнуйтесь, такие случаи тоже учитываются.\n\n"
            "⚠️ **ВНИМАНИЕ!**\n"
            "Повторная отправка чека или скриншота по одному и тому же донату через время — **СТРОГО ЗАПРЕЩЕНА.**\n"
            "За такие действия вы будете **навсегда заблокированы** в боте и канале. **Возврат средств невозможен.**\n\n"
            "**Если возникли сложности — просто напишите в личку: @galql.**",
            parse_mode='Markdown')

        context.user_data["awaiting_screenshot"] = None
    else:
        await update.message.reply_text("Неожиданное фото. Пожалуйста, следуйте инструкциям при покупке.")

# --- Запуск ---

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_menu))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    app.run_polling()

if __name__ == "__main__":
    main()
