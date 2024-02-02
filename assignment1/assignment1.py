import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def scrape_lines(character, soup):
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

def wordcloud_plot(lines1, lines2):
    wordcloud1 = WordCloud(width=600, height=200,background_color='white').generate(lines1)
    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud1)
    plt.axis('off')
    plt.show()

    wordcloud2 = WordCloud(width=600, height=200,background_color='white').generate(lines2)
    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud2)
    plt.axis('off')
    plt.show()

def main():
    godFather_link = "https://www.dailyscript.com/scripts/The_Godfather.html"
    godFather2_link = "https://www.dailyscript.com/scripts/godfather2.html"
    #LINKS FOR SCRAPING

    html_gf1 = requests.get(godFather_link)
    html_gf2 = requests.get(godFather2_link)
    #REQUESTS LINKS, SAVES IN VAR

    soup_gf1 = BeautifulSoup(html_gf1.text, features='html.parser')
    soup_gf2 = BeautifulSoup(html_gf2.text, features='html.parser')
    #TURN INTO BEAUTFIULSOUP OBJECTS

    michael_lines_gf1 = scrape_lines("MICHAEL", soup_gf1)
    michael_lines_gf2 = scrape_lines("MICHAEL", soup_gf2)
    #SCRAPE ALL LINES OF CHARACTER "MICHAEL"

    open("Godfather1.txt", "w", encoding="utf-8").write(michael_lines_gf1)
    open("Godfather2.txt", "w", encoding="utf-8").write(michael_lines_gf2)
    #WRITES SCRAPED LINES INTO TEXT FILES
    
    michael_lines_gf1 = michael_lines_gf1.replace('MICHAEL', '')
    michael_lines_gf2 = michael_lines_gf2.replace('MICHAEL', '')
    #PREPARATION FOR PLOT, GETTING RID OF MICHAEL

    wordcloud_plot(michael_lines_gf1,michael_lines_gf2)
    #WORLDCLOUD PLOT
main()

