import os
from nltk.tokenize import word_tokenize
import math
import re
#Import necessary libraries


def read_files_in_directory(directory_path): #read song and store it in a dictionary
    dic_genre_term_frequency = {}

    for genre in os.listdir(directory_path):
        dic_term_frequency = {}
        for song in os.listdir(f"{directory_path}/{genre}/"):
            with open(f"{directory_path}/{genre}/{song}", 'r') as rfile: #each song
                text = rfile.read().lower()
                text = re.sub(r'[^a-zA-Z ]', '', text)
                tokens = word_tokenize(text)
                for token in tokens:
                    dic_term_frequency[token] = dic_term_frequency.get(token, 0) + 1

        dic_genre_term_frequency[genre] = dic_term_frequency
        
    
    return dic_genre_term_frequency #nested dictionary with genre as key, terms relating to genre as value

def freq_to_prob(dic_term_frequency): #turn number of appearances into probability value (0-1)
    dic_term_prob = {}
    for genre, terms in dic_term_frequency.items(): #iterates through genre key and terms nested dictionary
        total_terms = sum(dic_term_frequency[genre].values())
        term_frequency = {token: (appearances / total_terms) for token, appearances in terms.items()}
        dic_term_prob[genre] = term_frequency

    return dic_term_prob #same nested dictionary format


def calculate_probability(dic_term_prob, input_text, genre): #turns probability into new prob given input text
    prob = 0.0
    input_text = word_tokenize(input_text)
    for term in input_text:
        if dic_term_prob[genre].get(term, 0) > 0:
            prob += math.log(dic_term_prob[genre].get(term))


    return prob #individual genre of probability

def unigramtraining(): #trains unigram model, this is included so you don't have to run the trainer individually each time
    path = "/Users/evankoenig/Downloads/TM_CA1_Lyrics2"
    for genre in os.listdir(path):
        dic = read_files_in_directory(f"{path}/")

    return dic #nested dictionary

def unigramrun(text, dic): #runs unigram given text and dictionary (unigramtraining dictionary)

    results = {}
    path = "/Users/evankoenig/Downloads/TM_CA1_Lyrics2"

    for genre in os.listdir(path):
        prob = freq_to_prob(dic)
        p = calculate_probability(prob, text, genre)
        results[genre] = p

    return results #dictionary of results for each genre

#To run individually
#dic = unigramtraining()
#print(unigramrun(text, dic))