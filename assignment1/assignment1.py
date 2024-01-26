import requests
from bs4 import BeautifulSoup


godFather_link = "https://www.dailyscript.com/scripts/The_Godfather.html"
godFather2_link = "https://www.dailyscript.com/scripts/godfather2.html"

html_gf1 = requests.get(godFather_link)
html_gf2 = requests.get(godFather2_link)

soup_gf1 = BeautifulSoup(html_gf1.text, features='html.parser')
soup_gf2 = BeautifulSoup(html_gf2.text, features='html.parser')

def extract_lines(character, soup):
    lines = []
    for tag in soup.find_all("b"):
        if tag.get_text().strip().lower() == character.lower():
            next_sibling = tag.find_next_sibling()
            while next_sibling and next_sibling.name != "b":
                lines.append(next_sibling.get_text().strip())
                next_sibling = next_sibling.find_next_sibling()
    return lines

michael_lines_gf1 = extract_lines("MICHAEL", soup_gf1)
michael_lines_gf2 = extract_lines("MICHAEL", soup_gf2)

with open("Godfather1_Michael.txt", "w", encoding="utf-8") as file:
    file.write("\n".join(michael_lines_gf1))

with open("Godfather2_Michael.txt", "w", encoding="utf-8") as file:
    file.write("\n".join(michael_lines_gf2))



