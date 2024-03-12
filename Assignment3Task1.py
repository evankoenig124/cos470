import requests
from bs4 import BeautifulSoup
import os
import csv
import re

def scrapesongs(path):
    with open('trainingdata.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Song Name', 'Genre', 'Lyrics'])
        for genre in os.listdir(path):
            if genre != '.DS_Store':
                if genre == 'Metal':
                    html = requests.get('https://www.popvortex.com/music/charts/top-heavy-metal-songs.php')
                else:
                    html = requests.get(f'https://www.popvortex.com/music/charts/top-{genre.lower()}-songs.php')
                soup = BeautifulSoup(html.text, features='html.parser')
                song_spans = soup.find_all('cite', class_='title')
                artist_spans = soup.find_all('em',class_='artist')
                for i in range(len(song_spans)):
                    song_name = re.sub(r'[^a-zA-Z]', '-', song_spans[i].text)
                    artist_name = re.sub(r'[^a-zA-Z]', '-', artist_spans[i].text)
                    lyricshtml = requests.get(f'https://genius.com/{artist_name}-{song_name}-lyrics')
                    lyricsoup = BeautifulSoup(lyricshtml.text, features='html.parser')
                    lyrics = lyricsoup.find('div', class_='Lyrics__Container-sc-1ynbvzw-1 kUgSbL')
                    if song_name not in path:
                        if lyrics:
                            csv_writer.writerow([song_name, artist_name,genre,lyrics.get_text(separator=' ')])

def main():
    testsongspath = "/Users/evankoenig/Downloads/Test Songs"
    scrapesongs(testsongspath)

if __name__ == "__main__":
    main()
