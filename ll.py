from bs4 import BeautifulSoup
import requests
import re


cinema = "https://30nama.ws/?s=kill+bill"
r = requests.get(cinema)
c = r.content

soup = BeautifulSoup(c, "html.parser")

data = soup.find_all("article", {"class": "post"})
if data:
    lasthope = 0
    for item in data:
        lasthope += 1
        title = item.find_next("h2").text
        cont = item.find_next("p").text

        pic = item.find_next('img', attrs={'src': re.compile("^https://")})
        photo = (link.get('src'))
        print(title)
        print(cont)
        print(photo)