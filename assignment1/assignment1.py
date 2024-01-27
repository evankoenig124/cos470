import requests
from bs4 import BeautifulSoup


godFather_link = "https://www.dailyscript.com/scripts/The_Godfather.html"
godFather2_link = "https://www.dailyscript.com/scripts/godfather2.html"

html_gf1 = requests.get(godFather_link)
html_gf2 = requests.get(godFather2_link)

soup_gf1 = BeautifulSoup(html_gf1.text, features='html.parser')
soup_gf2 = BeautifulSoup(html_gf2.text, features='html.parser')

def extract_lines(character, soup):
    script = soup.find("pre")
    script = script.get_text().splitlines()
    newscript = ''
    line = 0
    while line < len(script):
        if script[line].replace('\t', '') == character:
            while True:
                newscript += script[line] + '\n'
                line += 1
                if line >= len(script) or script[line] == '':
                    break
        line += 1
    return newscript

michael_lines_gf1 = extract_lines("MICHAEL", soup_gf1)
michael_lines_gf2 = extract_lines("MICHAEL", soup_gf2)

open("Godfather1.txt", "w", encoding="utf-8").write(michael_lines_gf1)
open("Godfather2.txt", "w", encoding="utf-8").write(michael_lines_gf2)



