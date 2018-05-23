import logging,pandas
from queue import Queue
from threading import Thread
from telegram import Bot
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Updater, Filters




logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
TOKEN = '569768947:AAGeaItAKWl3JolhuMdMhdcG4yRJCttFtZ8'


def start(bot, update):
    update.message.reply_text('با نوشتن عنوان فارسی یا انگلیسی فیلم میتوانید جستجو کنید')

def board(bot, update):

    bot = Bot(TOKEN)
    id = update.message.from_user.id
    id = int(id)
    #########
    user = update.message.from_user
    user = str(user)
    ###########


    try:


        df = pandas.read_excel('base.xlsx')
        # print the column names
        query = str(input("please enter the title: "))
        i = 0
        ecount = 0
        fcount = 0
        try:
            for item in df['title']:
                if query.lower() in str(item).lower():
                    ecount += 1
                    farsi = str(df['titlef'][i]) + " عنوان: "
                    bot.send_message(chat_id=id, text=farsi)

                    country = str(df['country'][i]) + " کشور: "
                    bot.send_message(chat_id=id, text=country)

                    genre = str(df['genre'][i]) + " سبک: "
                    bot.send_message(chat_id=id, text=genre)

                    year = str(df['year'][i]) + " سال: "
                    bot.send_message(chat_id=id, text=year)

                    cast = str(df['cast'][i]) + " بازیگران: "
                    bot.send_message(chat_id=id, text=cast)


                    director = str(df['director'][i]) + " کارگردان "
                    bot.send_message(chat_id=id, text=director)

                    details = str(df['details'][i])
                    bot.send_message(chat_id=id, text=details)

                i += 1
        except:
            pass
        try:
            j = 0
            for item in df['titlef']:
                if query in str(item):
                    fcount += 1
                    eng = str(df['title'][i]) + " عنوان: "
                    bot.send_message(chat_id=id, text=eng)

                    country = str(df['country'][i]) + " کشور: "
                    bot.send_message(chat_id=id, text=country)

                    genre = str(df['genre'][i]) + " سبک: "
                    bot.send_message(chat_id=id, text=genre)

                    year = str(df['year'][i]) + " سال: "
                    bot.send_message(chat_id=id, text=year)

                    cast = str(df['cast'][i]) + " بازیگران: "
                    bot.send_message(chat_id=id, text=cast)

                    director = str(df['director'][i]) + " کارگردان "
                    bot.send_message(chat_id=id, text=director)

                    details = str(df['details'][i])
                    bot.send_message(chat_id=id, text=details)

                j += 1
        except:
            pass
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
        print("failed")




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
        dp.add_handler(MessageHandler(Filters.text, board))

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