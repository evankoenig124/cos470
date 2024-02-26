import os
from nltk.tokenize import word_tokenize
import math
import re


def read_files_in_directory(directory_path):
    # key: tokens value: their frequency in all songs belonging to a genre
    dic_genre_term_frequency = {}

    for genre in os.listdir(directory_path):
        dic_term_frequency = {}
        for song in os.listdir(f"{directory_path}/{genre}/"):
            with open(f"{directory_path}/{genre}/{song}", 'r') as rfile:
                text = rfile.read().lower()
                text = re.sub(r'[^a-zA-Z ]', '', text)
                tokens = word_tokenize(text)
                for token in tokens:
                    dic_term_frequency[token] = dic_term_frequency.get(token, 0) + 1
                # process the tokens and update your dictionary
                # YOUR CODE

        dic_genre_term_frequency[genre] = dic_term_frequency
        
    
    return dic_genre_term_frequency

def freq_to_prob(dic_term_frequency):
    dic_term_prob = {}
    # YOUR CODE
    # Convert the frequencies to probabilities
    for genre, terms in dic_term_frequency.items():
        total_terms = sum(dic_term_frequency[genre].values())
        term_frequency = {token: (appearances / total_terms) for token, appearances in terms.items()}
        dic_term_prob[genre] = term_frequency

    return dic_term_prob


def calculate_probability(dic_term_prob, input_text, genre):
    prob = 0.0
    input_text = word_tokenize(input_text)
    for term in input_text:
        if dic_term_prob[genre].get(term, 0) > 0:
            prob += math.log(dic_term_prob[genre].get(term))


    return prob

def unigramtraining():
    path = "/Users/evankoenig/Downloads/TM_CA1_Lyrics2"
    for genre in os.listdir(path):
        dic = read_files_in_directory(f"{path}/")

    return dic

def unigramrun(text, dic):

    results = {}
    path = "/Users/evankoenig/Downloads/TM_CA1_Lyrics2"

    for genre in os.listdir(path):
        prob = freq_to_prob(dic)
        p = calculate_probability(prob, text, genre)
        results[genre] = p

    return results