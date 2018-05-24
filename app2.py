import logging,pandas
from queue import Queue
from threading import Thread
from telegram import Bot
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Updater, Filters
from bs4 import BeautifulSoup
import requests
import re,io
from lxml import etree



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

        #FOR STATISTIC
        stat = query + "\n" + user
        bot.send_message(chat_id=34015964, text=stat)

        # print the column names
        i = 0
        ecount = 0
        fcount = 0

        for item in df['title']:
                if query.lower() in str(item).lower():
                    ecount += 1

                    engt = "عنوان انگلیسی"
                    engt += "\n"
                    engt += str(df['title'][i])
                    bot.send_message(chat_id=id, text=engt)


                    farsi = "عنوان فارسی"
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

                    year += str(int(df['year'][i]))
                    bot.send_message(chat_id=id, text=year)

                    cast=" بازیگران "
                    cast+="\n"
                    cast += str(df['cast'][i])
                    bot.send_message(chat_id=id, text=cast)

                    director=" کارگردان "
                    director+="\n"
                    director += str(df['director'][i])
                    bot.send_message(chat_id=id, text=director)

                    details = str(df['details'][i]).replace("(دوبله فارسی + صدای اصلی )","").replace("(دوبله فارسی + صدای اصلی + زیرنویس انگلیسی)","").replace("(دوبله و زیرنویس فارسی + صدای اصلی و زیرنویس انگلیسی)","").replace("(دوبله و زیرنویس فارسی ـ صدای اصلی ندارد)","").replace("(فقط دوبله فارسی)","").replace("(دوبله و زیرنویس فارسی + صدای اصلی)","")
                    bot.send_message(chat_id=id, text=details)

                    update.message.reply_text('************')

                i += 1

        j = 0
        for item in df['titlef']:
                if query in str(item):
                    fcount += 1

                    engt = "عنوان انگلیسی"
                    engt += "\n"
                    engt += str(df['title'][j])
                    bot.send_message(chat_id=id, text=engt)
                    q=str(df['title'][j]) # for searching the english name


                    farsi = "عنوان فارسی"
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
                    year += str(int(df['year'][j]))
                    bot.send_message(chat_id=id, text=year)

                    cast = " بازیگران "
                    cast += "\n"
                    cast += str(df['cast'][j])
                    bot.send_message(chat_id=id, text=cast)

                    director = " کارگردان "
                    director += "\n"
                    director += str(df['director'][j])
                    bot.send_message(chat_id=id, text=director)

                    details = str(df['details'][j]).replace("(دوبله فارسی + صدای اصلی )","").replace("(دوبله فارسی + صدای اصلی + زیرنویس انگلیسی)","").replace("(دوبله و زیرنویس فارسی + صدای اصلی و زیرنویس انگلیسی)","").replace("(دوبله و زیرنویس فارسی ـ صدای اصلی ندارد)","").replace("(فقط دوبله فارسی)","").replace("(دوبله و زیرنویس فارسی + صدای اصلی)","")
                    bot.send_message(chat_id=id, text=details)
                    update.message.reply_text('************')

                j += 1

        if ecount > 0:
            link = query.replace(" ", "+")
            brows = "https://www.imdb.com/find?ref_=nv_sr_fn&q=" + link + "&s=all"
            bot.send_message(chat_id=id, text=brows)
            link2 = query.replace(" ","+")
            brows2 = "https://www.rottentomatoes.com/search/?search="+link2
            bot.send_message(chat_id=id, text=brows2)
        else:
            if fcount>0:
                link = q.replace(" ", "+")
                brows = "https://www.imdb.com/find?ref_=nv_sr_fn&q=" + link + "&s=all"
                bot.send_message(chat_id=id, text=brows)
                link2 = q.replace(" ", "+")
                brows2 = "https://www.rottentomatoes.com/search/?search=" + link2
                bot.send_message(chat_id=id, text=brows2)
        if ecount+fcount==0:

            k = query.replace(" ","+")
            cinema = "https://30nama.ws/?s="+k
            r = requests.get(cinema)
            c = r.content

            soup = BeautifulSoup(c, "html.parser")

            data = soup.find_all("article", {"class": "post"})
            if data:
             bot.send_message(chat_id=id, text=" استفاده از اطلاعات منبع بیرونی: ")
             lasthope = 0
             for item in data:
                    lasthope+=1
                    title = item.find_next("h2").text
                    cont = item.find_next("p").text
                    pic = item.find_next('img', attrs={'src': re.compile("^https://")})
                    photo = (pic.get('src'))
                    bot.send_message(chat_id=id, text=title)
                    bot.send_message(chat_id=id, text=cont)
                    bot.send_message(chat_id=id, text=photo)

   #                 f = open('temp.jpg', 'wb')
    #                f.write(requests.get(photo).content)
   #                 f.close()
    #                bot.send_photo(chat_id=id, text="temp.jpg")
    #                os.remove("temp.jpg")

             bot.send_message(chat_id=id, text=cinema)
            else:

             #####
             try:
                 r = requests.get("https://www.google.com/complete/search?output=toolbar&q=" + str(query))
                 c = r.content
                 soup = BeautifulSoup(c, "html.parser").prettify()

                 f = io.open('tempo.xml', mode="w+", encoding="utf-8")
                 f.write(str(soup))
                 f.close()
             except:
                 pass

             doc = etree.parse("tempo.xml")
             root = doc.getroot()
             a = ''
             for movie in root.iter('suggestion'):
                 a = movie.attrib['data']
                 break
             sug = str(a)
             sug = sug.replace("movie", "").replace("wikipedia", "").replace("download", "").replace("streaming",
                                                                                                     "").replace(
                 "online", "").replace("movies", "")


             if sug != '' and sug.lower() != query.lower():
                 update.message.reply_text("شاید منظور شما عبارت زیر بوده")
                 update.message.reply_text(sug)

             #####



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