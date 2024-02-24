import os
import nltk
from nltk.tokenize import word_tokenize
import math
nltk.download('punkt')
from collections import defaultdict


def read_files_in_directory(directory_path):
    # key: tokens value: their frequency in all songs belonging to a genre
    dic_term_frequency = defaultdict(int)

    for file in os.listdir(directory_path):
        with open(directory_path + file, 'r') as rfile:
            for line in rfile:
                current_line = line.strip()
                tokens = word_tokenize(current_line)
                for token in tokens:
                    dic_term_frequency[token.lower()] += 1
                # process the tokens and update your dictionary
                # YOUR CODE

    return dic_term_frequency


def freq_to_prob(dic_term_frequency):
    dic_term_prob = {}
    # YOUR CODE
    # Convert the frequencies to probabilities
    total_terms = sum(dic_term_frequency.values())
    for term in dic_term_frequency:
        dic_term_prob[term] = ((dic_term_frequency[term] * 1.0) / total_terms)

    return dic_term_prob


def calculate_probability(dic_term_prob, input_text):
    prob = 0.0
    input_text = word_tokenize(input_text)
    for term in input_text:
        if dic_term_prob.get(term, 0) > 0:
            prob += math.log(dic_term_prob.get(term))


    return prob


def unigramrun(text):

    results = {}
    path = "/Users/evankoenig/Downloads/TM_CA1_Lyrics2"

    for genre in os.listdir(path):
        dic = read_files_in_directory(f"{path}/{genre}/")
        prob = freq_to_prob(dic)
        p = calculate_probability(prob, text)
        results[genre] = p
    #sorted_dict = dict(sorted(results.items(), key=lambda item: item[1], reverse=False))
    #for key in sorted_dict:
        #print(f"{key}: {sorted_dict[key]}")
    return results
