import logging,pandas
from queue import Queue
from threading import Thread
from telegram import Bot
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Updater, Filters




logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
TOKEN = '569768947:AAGeaItAKWl3JolhuMdMhdcG4yRJCttFtZ8'

df = pandas.read_excel('base.xlsx')

def start(bot, update):
    update.message.reply_text('با نوشتن عنوان فارسی یا انگلیسی فیلم میتوانید جستجو کنید')

def echo(bot, update):
    try:
        global df
        bot = Bot(TOKEN)
        id = update.message.from_user.id
        id = int(id)
        #########
        user = update.message.from_user
        user = str(user)
        ###########

        query = str(update.message.text)


        # print the column names
        i = 0
        ecount = 0
        fcount = 0

        for item in df['title']:
                if query.lower() in str(item).lower():
                    ecount += 1
                    farsi = "عنوان"
                    farsi+="\n"
                    farsi+= str(df['titlef'][i])
                    bot.send_message(chat_id=id, text=farsi)

                    country=" کشور "
                    country+="\n"
                    country += str(df['country'][i])
                    bot.send_message(chat_id=id, text=country)

                    genre= " ژانر "
                    genre+="\n"
                    genre += str(df['genre'][i])
                    bot.send_message(chat_id=id, text=genre)

                    year =" سال "
                    year+="\n"
                    year += str(df['year'][i])
                    bot.send_message(chat_id=id, text=year)

                    cast=" بازیگران "
                    cast+="\n"
                    cast += str(df['cast'][i])
                    bot.send_message(chat_id=id, text=cast)

                    director=" کارگردان "
                    director+="\n"
                    director += str(df['director'][i])
                    bot.send_message(chat_id=id, text=director)

                    details = str(df['details'][i])
                    bot.send_message(chat_id=id, text=details)

                i += 1

        j = 0
        for item in df['titlef']:
                if query in str(item):
                    fcount += 1
                    farsi = "عنوان"
                    farsi += "\n"
                    farsi += str(df['titlef'][j])
                    bot.send_message(chat_id=id, text=farsi)

                    country = " کشور "
                    country += "\n"
                    country += str(df['country'][j])
                    bot.send_message(chat_id=id, text=country)

                    genre = " ژانر "
                    genre += "\n"
                    genre += str(df['genre'][j])
                    bot.send_message(chat_id=id, text=genre)

                    year = " سال "
                    year += "\n"
                    year += str(df['year'][j])
                    bot.send_message(chat_id=id, text=year)

                    cast = " بازیگران "
                    cast += "\n"
                    cast += str(df['cast'][j])
                    bot.send_message(chat_id=id, text=cast)

                    director = " کارگردان "
                    director += "\n"
                    director += str(df['director'][j])
                    bot.send_message(chat_id=id, text=director)

                    details = str(df['details'][j])
                    bot.send_message(chat_id=id, text=details)

                j += 1

        if ecount > 0:
            link = query.replace(" ", "+")
            brows = "https://www.imdb.com/find?ref_=nv_sr_fn&q=" + link + "&s=all"
            bot.send_message(chat_id=id, text=brows)
            link2 = query.replace(" ","+")
            brows2 = "https://www.rottentomatoes.com/search/?search="+link2
            bot.send_message(chat_id=id, text=brows2)

        if ecount+fcount==0:
            update.message.reply_text("موردی یافت نشد لینک زیر را چک کنید همچنین میتواند داستان فیلم و بازیگران آن را به انگلیسی بنویسید و جستجو را تکرار کنید تا از طریق لینک پایین حدس بهتری زده شود")
            x = query.replace(" ","+")
            ai = "https://www.whatismymovie.com/results?text="+x
            bot.send_message(chat_id=id, text=ai)


    except:
        pass

def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))

# Write your handlers here


def setup(webhook_url=None):
    """If webhook_url is not passed, run with long-polling."""
    logging.basicConfig(level=logging.WARNING)
    if webhook_url:
        bot = Bot(TOKEN)
        update_queue = Queue()
        dp = Dispatcher(bot, update_queue)
    else:
        updater = Updater(TOKEN)
        bot = updater.bot
        dp = updater.dispatcher
        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(CommandHandler("help", start))

        # on noncommand i.e message - echo the message on Telegram
        dp.add_handler(MessageHandler(Filters.text, echo))

        # log all errors
        dp.add_error_handler(error)
    # Add your handlers here
    if webhook_url:
        bot.set_webhook(webhook_url=webhook_url)
        thread = Thread(target=dp.start, name='dispatcher')
        thread.start()
        return update_queue, bot
    else:
        bot.set_webhook()  # Delete webhook
        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
    setup()