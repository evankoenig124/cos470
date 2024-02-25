import os
import nltk
from nltk.tokenize import word_tokenize
import math
import re
nltk.download('punkt')
from collections import defaultdict


def read_files_in_directory(directory_path):
    # Precompile regular expression pattern
    regex_pattern = re.compile("[^A-Za-z\s]")

    # Initialize dictionaries
    dic_term_frequency = defaultdict(int)
    dic_pairs_frequency = defaultdict(int)

    for file in os.listdir(directory_path):
        with open(os.path.join(directory_path, file), 'r') as rfile:
            for line in rfile:
                current_line = regex_pattern.sub("", line.strip().lower())
                tokens = word_tokenize(current_line)
                
                if tokens:
                    # Update frequency dictionaries
                    dic_pairs_frequency[f"<s> {tokens[0]}"] += 1
                    for i in range(len(tokens)-1):
                        dic_term_frequency[tokens[i]] += 1
                        dic_pairs_frequency[f"{tokens[i]} {tokens[i+1]}"] += 1
                    dic_pairs_frequency[f"{tokens[-1]} </s>"] += 1


    return dic_term_frequency, dic_pairs_frequency


def freq_to_prob(dic_term_frequency, dic_pairs_frequency):
    dic_term_prob = {}
    
    for term in dic_pairs_frequency:
        bottomterm = word_tokenize(term)
        bottomterm = term[0]
        if dic_term_frequency[bottomterm]:
            dic_term_prob[term] = (((dic_pairs_frequency[term] * 1.0) + 1)/(dic_term_frequency[bottomterm]+ len(dic_pairs_frequency)))

    return dic_term_prob


def calculate_probability(dic_term_prob, input_text):
    prob = 0.0
    input_text = word_tokenize(input_text)
    for i in range(len(input_text)-1):
        input_text[i] = input_text[i].lower() + " " + input_text[i+1].lower()
    for term in input_text:
        if dic_term_prob.get(term, 0) > 0:
            prob += math.log(dic_term_prob.get(term))


    return prob


def bigramrun(text):
    results = {}
    path = "/Users/evankoenig/Downloads/TM_CA1_Lyrics2"

    for genre in os.listdir(path):
        dic1, dic2 = read_files_in_directory(f"{path}/{genre}/")
        prob = freq_to_prob(dic1, dic2)
        p = calculate_probability(prob, text)
        results[genre] = p
    #sorted_dict = dict(sorted(results.items(), key=lambda item: item[1], reverse=False))
    #for key in sorted_dict:
        #print(f"{key}: {sorted_dict[key]}")
    return results

#print(bigramrun("""You used to call me on my cell phone
#Late night when you need my love
#Call me on my cell phone"""))