import requests
from bs4 import BeautifulSoup
import os
import csv

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
                for span in song_spans:
                    song_name = span.text.strip()
                    if song_name not in path:
                        csv_writer.writerow([song_name, genre])

def main():
    testsongspath = "/Users/evankoenig/Downloads/Test Songs"
    scrapesongs(testsongspath)

if __name__ == "__main__":
    main()
