from bs4 import BeautifulSoup
import requests,re


r = requests.get("https://30nama.ws/?s=yoyoyoyoy+rrrkjf")
c = r.content

soup = BeautifulSoup(c, "html.parser")

data = soup.find_all("article", {"class": "post"})

if data:
    print("not empty")
else:
    print("empty")
for item in data:

    cont = item.find_next("p").text
    title = item.find_next("h2").text

    print(title)
    print(cont)

