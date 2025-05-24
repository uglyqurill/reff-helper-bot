import os
from dotenv import load_dotenv
import telebot

from crossref_client import fetch_metadata_by_doi, CrossrefError
from formatter import format_book, format_article, format_electronic, format_chapter

# 1) Загружаем токен
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
print("Loaded BOT_TOKEN:", BOT_TOKEN)

# 2) Инициализируем бота
bot = telebot.TeleBot(BOT_TOKEN)
bot.remove_webhook()


# 3) Хендлер для /start и /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    text = (
        "Привет! Я — ReffHelperBot. 🤖\n\n"
        "Отправь мне DOI (например, `10.1038/nphys1170`),\n"
        "и я верну библиографическое описание по ГОСТ Р 7.0.5–2008."
    )
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

# 4) Обработчик DOI
@bot.message_handler(func=lambda msg: True)
def handle_doi(message):
    doi = message.text.strip()
    try:
        meta = fetch_metadata_by_doi(doi)
    except CrossrefError as e:
        return bot.send_message(message.chat.id, f"❌ {e}")

    # Выбор шаблона по типу ресурса
    rtype = meta.get("type", "")
    if rtype == "book":
        desc = format_book(meta)
    elif rtype == "journal-article":
        desc = format_article(meta)
    elif rtype in ("book-chapter", "chapter"):  # глава книги/сборника
        desc = format_chapter(meta)
    else:
        desc = format_electronic(meta)

    # Отправляем оформленное описание
    bot.send_message(message.chat.id, desc)

# 5) Запуск
if __name__ == '__main__':
    bot.remove_webhook()
    print("Bot is polling...")
    bot.infinity_polling(skip_pending=True)

