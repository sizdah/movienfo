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


    ### Import Beautiful Soup
    ### Here, I have the BeautifulSoup folder in the level of this Python script
def downloadlink(w):
    fail = 0
    result = ''

   # try:

#        q2 = w.replace(" ", "+")
  #      base2 = "https://dibamoviez.top/?s=" + q2
   #     r2 = requests.get(base2)
    #    page2 = r2.content
     #   soup2 = BeautifulSoup(page2, 'html.parser')

     #   vv2 = soup2.find_all('div', attrs={'class': 'search-results'})

      #  list2 = []
      #  for v2 in vv2:
       #     link2 = v2.find_next('a', attrs={'href': re.compile("^https://")})
        #    url2 = link2.get('href')
         #   list2.append(url2)
        #try:
         #   result = str((list2[0]))
        #except:
        #    fail = fail + 1

       # if fail != 1:
         #   return result
        #else:
          #  pass
    #except:
       # pass

    try:
        q = w.replace(" ", "+")
        base = "http://www.film2movie.us/search/" + q
        r = requests.get(base)
        page = r.content
        soup = BeautifulSoup(page, 'html.parser')

        vv = soup.find_all('div', attrs={'class': 'title'})

        if "مورد درخواستی در این سایت وجود ندارد" in str(vv):
            fail = fail + 1

        list = []
        for v in vv:
            link = v.find_next('a', attrs={'href': re.compile("^http://")})
            url = link.get('href')
            list.append(url)
        if fail < 2:
            return str((list[1]))
    except:
        pass




    try:

            q3 = w.replace(" ", "+")
            base3 = "http://www.avadl.me/?s=" + q3
            r3 = requests.get(base3)
            page3 = r3.content
            soup3 = BeautifulSoup(page3, 'html.parser')
            vv3 = soup3.find_all('h2')
            try:
                link3 = vv3[1].find_next('a', attrs={'href': re.compile("^http://")})
                url3 = link3.get('href')
                result = url3
            except:
                fail = fail + 1

            if fail < 3:
                return result

    except:
        pass

    try:
        k = w.replace(" ", "+")
        cinema = "https://30nama.win/?s=" + k
        r = requests.get(cinema)
        c = r.content

        soup = BeautifulSoup(c, "html.parser")

        data = soup.find_all("article", {"class": "post"})
        l=[]
        for item in data:
            dl = item.find_next("a", attrs={'href': re.compile("^https://")})
            fdl = dl.get('href')
            l.append(fdl)
            break
        try:
            return l[0]
        except:
            return False

    except:
        return False
def youtube(q):
    base = "https://www.youtube.com/results?search_query="
    qstring = str(q)+" movie trailer"
    qstring = qstring.replace(" ","+")

    r = requests.get(base + qstring)
    page = r.content
    soup = BeautifulSoup(page, 'html.parser')

    vids = soup.findAll('a', attrs={'class': 'yt-uix-tile-link'})
    v = vids[0]
    tmp = 'https://www.youtube.com' + v['href']
    tmp = str(tmp)
    return tmp


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
        j=i
        ecount = 0
        fcount = 0

        for item in df['title']:
                if query.lower() in str(item).lower():
                    ecount += 1

                    engt = "عنوان انگلیسی:"
                    engt += "\n"
                    engt += str(df['title'][i])

                    engt += "\n\n"

                    engt += "عنوان فارسی:"
                    engt+="\n"
                    engt+= str(df['titlef'][i])

                    engt += "\n\n"

                    engt+=" کشور: "
                    engt+="\n"
                    engt += str(df['country'][i])
                    engt += "\n\n"

                    engt+= " ژانر: "
                    engt+="\n"
                    engt += str(df['genre'][i])

                    engt += "\n\n"

                    engt +=" سال: "
                    engt +="\n"
                    engt += str(int(df['year'][i]))
                    engt += "\n\n"

                    engt+=" بازیگران: "
                    engt+="\n"
                    engt += str(df['cast'][i])
                    engt += "\n\n"

                    engt+=" کارگردان: "
                    engt+="\n"
                    engt += str(df['director'][i])
                    engt += "\n\n"

                    engt += str(df['details'][i]).replace("(دوبله فارسی + صدای اصلی )","").replace("(دوبله فارسی + صدای اصلی + زیرنویس انگلیسی)","").replace("(دوبله و زیرنویس فارسی + صدای اصلی و زیرنویس انگلیسی)","").replace("(دوبله و زیرنویس فارسی ـ صدای اصلی ندارد)","").replace("(فقط دوبله فارسی)","").replace("(دوبله و زیرنویس فارسی + صدای اصلی)","")
                    bot.send_message(chat_id=id, text=engt)

                    info = "در صورت تمایل با فروارد این تریلر به ربات @getmediabot میتوانید این ویدئو را دانلود کنید "
                    info += "\n"
                    vv = youtube(str(df['title'][i]))
                    bot.send_message(chat_id=id, text=info)
                    bot.send_message(chat_id=id, text=vv)

                    key = downloadlink(str(df['title'][i]))
                    if key:
                        downinfo = "لینک زیر برای دانلود فیلم پیدا شد"
                        downinfo+="\n"
                        downinfo += key
                        bot.send_message(chat_id=id, text=downinfo)


                i += 1


        for item in df['titlef']:
                if query in str(item):
                    fcount += 1

                    engt = "عنوان انگلیسی:"
                    engt += "\n"
                    engt += str(df['title'][j])

                    engt += "\n\n"

                    engt += "عنوان فارسی:"
                    engt += "\n"
                    engt += str(df['titlef'][j])

                    engt += "\n\n"

                    engt += " کشور: "
                    engt += "\n"
                    engt += str(df['country'][j])
                    engt += "\n\n"

                    engt += " ژانر: "
                    engt += "\n"
                    engt += str(df['genre'][j])

                    engt += "\n\n"

                    engt += " سال: "
                    engt += "\n"

                    engt += str(int(df['year'][j]))
                    engt += "\n\n"

                    engt += " بازیگران: "
                    engt += "\n"
                    engt += str(df['cast'][j])

                    engt += "\n\n"

                    engt += " کارگردان: "
                    engt += "\n"
                    engt += str(df['director'][j])
                    engt += "\n\n"

                    engt += str(df['details'][j]).replace("(دوبله فارسی + صدای اصلی )", "").replace(
                        "(دوبله فارسی + صدای اصلی + زیرنویس انگلیسی)", "").replace(
                        "(دوبله و زیرنویس فارسی + صدای اصلی و زیرنویس انگلیسی)", "").replace(
                        "(دوبله و زیرنویس فارسی ـ صدای اصلی ندارد)", "").replace("(فقط دوبله فارسی)", "").replace(
                        "(دوبله و زیرنویس فارسی + صدای اصلی)", "")
                    bot.send_message(chat_id=id, text=engt)
                    info = "در صورت تمایل با فروارد این تریلر به ربات @getmediabot میتوانید این ویدئو را دانلود کنید "
                    info+="\n"
                    vv=youtube(str(df['title'][j]))
                    bot.send_message(chat_id=id, text=info)
                    bot.send_message(chat_id=id, text=vv)

                    key = downloadlink(str(df['title'][j]))
                    if key:
                        downinfo = "لینک زیر برای دانلود فیلم پیدا شد"
                        downinfo += "\n"
                        downinfo += key
                        bot.send_message(chat_id=id, text=downinfo)

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
                link = query.replace(" ", "+")
                brows = "https://www.imdb.com/find?ref_=nv_sr_fn&q=" + link + "&s=all"
                bot.send_message(chat_id=id, text=brows)
                link2 = query.replace(" ", "+")
                brows2 = "https://www.rottentomatoes.com/search/?search=" + link2
                bot.send_message(chat_id=id, text=brows2)
        if ecount+fcount==0:

            k = query.replace(" ","+")
            cinema = "https://30nama.fun/?s="+k
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


                    mes = str(title) + "\n\n" + str(cont)
                    bot.send_message(chat_id=id, text=mes)
                    bot.send_message(chat_id=id, text=photo)
                    info = "در صورت تمایل با فروارد این تریلر به ربات @getmediabot میتوانید این ویدئو را دانلود کنید "
                    bot.send_message(chat_id=id, text=info)
                    bot.send_message(chat_id=id, text=youtube(str(title)))

                    key = downloadlink(str(title))
                    if key:
                        downinfo = "لینک زیر برای دانلود فیلم پیدا شد"
                        downinfo += "\n"
                        downinfo += key
                        bot.send_message(chat_id=id, text=downinfo)




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
