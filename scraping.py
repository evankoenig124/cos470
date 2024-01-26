import requests
from bs4 import BeautifulSoup


godFather_link = "https://www.dailyscript.com/scripts/The_Godfather.html"
godFather2_link = "https://www.dailyscript.com/scripts/godfather2.html"


html_gf1 = requests.get(godFather_link)
html_gf2 = requests.get(godFather2_link)
soup_gf1 = BeautifulSoup(html_gf1.text)
soup_gf2 = BeautifulSoup(html_gf2.text)

print(soup_gf1)
print(soup_gf2)
