import os
from nltk.tokenize import word_tokenize
import math
import re
#import necessary dictionaries

def read_files_in_directory(directory_path): #read all songs and store it in a dictionary
    dic_genre_term_frequency = {}
    dic_genre_pairs_frequency = {}
    for genre in os.listdir(directory_path):
        dic_term_frequency = {}
        dic_pairs_frequency = {}
        for song in os.listdir(f"{directory_path}/{genre}/"):
            with open(f"{directory_path}/{genre}/{song}", 'r') as rfile:
                for line in rfile:
                    line = line.lower()
                    line = re.sub(r'[^a-zA-Z ]', '', line)
                    tokens = word_tokenize(line)
                    if tokens != []:
                        dic_pairs_frequency[f"<s> {tokens[0]}"] = dic_pairs_frequency.get(f"<s> {tokens[0]}", 0) + 1 #first line
                        for i in range(len(tokens)-1):
                            dic_term_frequency[tokens[i]] = dic_term_frequency.get(tokens[i], 0) + 1
                            dic_pairs_frequency[f"{tokens[i]} {tokens[i+1]}"] = dic_pairs_frequency.get(f"{tokens[i]} {tokens[i+1]}", 0) + 1 #create pairs
                        dic_pairs_frequency[f"{tokens[-1]} </s>"] = dic_pairs_frequency.get(f"{tokens[-1]} </s>", 0) + 1 #last line
        dic_genre_term_frequency[genre] = dic_term_frequency
        dic_genre_pairs_frequency[genre] = dic_pairs_frequency


    return dic_genre_term_frequency, dic_genre_pairs_frequency #returns nested dictionaries with genre as keys and terms relating to genre as values


def freq_to_prob(dic_term_frequency, dic_pairs_frequency): #turn number of appearances into probability value (0-1)
    dic_term_prob = {}
    for genre, terms in dic_pairs_frequency.items():
        if genre not in dic_term_prob:
            dic_term_prob[genre] = {}
        
        for token in terms:
            bottomterm = token.split()
            bottomterm = bottomterm[0] #first term for +1 equation
            if bottomterm in dic_term_frequency[genre].keys():
                term_frequency = (((dic_pairs_frequency[genre][token] * 1.0) + 1)/(dic_term_frequency[genre][bottomterm]+ len(dic_pairs_frequency)))
                dic_term_prob[genre][token] = term_frequency #create probabilities with +1 equation

    return dic_term_prob #nested dictionary (genre: terms dictionary)


def calculate_probability(dic_term_prob, input_text, genre): #make probability for text being part of genre
    prob = 0.0
    input_text = input_text.lower()
    input_text = word_tokenize(input_text)
    for i in range(len(input_text)-1):
        input_text[i] = input_text[i] + " " + input_text[i+1] #turning input text into pairs
    for term in input_text:
        if dic_term_prob[genre].get(term, 0) > 0:
            prob += math.log(dic_term_prob[genre].get(term)) 

    return prob #genre probability of text being part of genre

def bigramtraining():
    path = "/Users/evankoenig/Downloads/TM_CA1_Lyrics2"
    for genre in os.listdir(path):
        dic1, dic2 = read_files_in_directory(f"{path}/")
    
    return dic1, dic2

def bigramrun(text, dic1, dic2):
    results = {}
    path = "/Users/evankoenig/Downloads/TM_CA1_Lyrics2"

    for genre in os.listdir(path):
        prob = freq_to_prob(dic1, dic2)
        p = calculate_probability(prob, text, genre)
        results[genre] = p
    return results

#To run individually
#dic1, dic2 = bigramtraining()
#print(bigramrun(text, dic))