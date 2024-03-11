from BigramModel import bigramrun, bigramtraining
from UnigramModel import unigramrun, unigramtraining
import os
import csv
import scipy.stats as stats
#import necessary libraries

UNIDIC = unigramtraining()
BIDIC1, BIDIC2 = bigramtraining()
#dictionaries are referenced here so they don't need to be called in each function call

def find_best_lambda(directory_path): #finds best lambda using given equation
    highest_correct_predictions = 0
    best_lambda_value = 0
        
    for i in range(11):
        lambda_value = i / 10.0 #0.0-1 values
        current_correct_predictions = 0
        
        for file in os.listdir(directory_path):
            if file.endswith('.txt'):
                with open(os.path.join(directory_path, file), 'r') as file:
                    actual_genre = file.readline()
                    actual_genre = actual_genre.strip()
                    text = file.read()
                    unigram_results = unigramrun(text, UNIDIC)
                    bigram_results = bigramrun(text, BIDIC1, BIDIC2) #run each model

                    combined_results = {}
                    for genre in unigram_results: #calculate mixed values using given equation
                        combined_probability = (lambda_value * unigram_results[genre]) + ((1 - lambda_value) * bigram_results[genre])
                        combined_results[genre] = combined_probability
                    
                    if min(combined_results, key=combined_results.get) == actual_genre: #min() gives the most probable
                        current_correct_predictions += 1

        if highest_correct_predictions <= current_correct_predictions: #finds best lambda (even in lambdas are equal)
            highest_correct_predictions = current_correct_predictions
            best_lambda_value = lambda_value
                
    return best_lambda_value #best lambda 0.0-1

def goldlabelresults(path, lambda_value): #tests gold labels with all 3 models
    unigram_results = {}
    bigram_results = {}
    mixed_results = {}
    i = 0

    with open(path, 'r', newline='') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        for song in reader:
            unigram_line = unigramrun(song[1], UNIDIC)
            bigram_line = bigramrun(song[1], BIDIC1, BIDIC2)
            mixed_line = {}
            for genre in unigram_line: #finds mixedmodel probability
                combined_probability = (lambda_value * unigram_line[genre]) + ((1 - lambda_value) * bigram_line[genre])
                mixed_line[genre] = combined_probability
            unigram_results[i] = unigram_line
            bigram_results[i] = bigram_line
            mixed_results[i] = mixed_line
            i += 1
    
    return unigram_results, bigram_results, mixed_results #result dictionaries for all 3 models

def calculate_f1(unigram, bigram, mixed, path): #finds f1 scores for each model
    unitp = 0
    unifp = 0
    unifn = 0

    bitp = 0
    bifp = 0
    bifn = 0

    mixtp = 0
    mixfp = 0
    mixfn = 0
    #intitialization of true pos, false pos, and false neg

    with open(path, 'r', newline='') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        for song in reader:
            for id in unigram:
                # Unigram
                if min(unigram[id], key=unigram[id].get) == song[2]: #if most probable is correct
                    unitp += 1
                else:
                    if unigram.get(id, {}).get(song[2], 0) == 0: #if in dic but no odds
                        unifn += 1
                    else: #else with odds but wrong
                        unifp += 1
                
                # Bigram
                if min(bigram[id], key=bigram[id].get) == song[2]:
                    bitp += 1
                else:
                    if bigram.get(id, {}).get(song[2], 0) == 0:
                        bifn += 1
                    else:
                        bifp += 1
                
                # Mixed
                if min(mixed[id], key=mixed[id].get) == song[2]:
                    mixtp += 1
                else:
                    if mixed.get(id, {}).get(song[2], 0) == 0:
                        mixfn += 1
                    else:
                        mixfp += 1  
    print(unitp, unifn, unifp)
    print(bitp,bifn, unifp)
    print(mixtp, mixfn, mixfp)
    unif1 = (2*(unitp/(unitp+unifp))*(unitp/(unitp+unifn))) / (unitp/(unitp+unifp) + unitp/(unitp+unifn))
    bif1 = (2*(bitp/(bitp+bifp))*(bitp/(bitp+bifn))) / (bitp/(bitp+bifp) + bitp/(bitp+bifn))
    mixf1 = (2*(mixtp/(mixtp+mixfp))*(mixtp/(mixtp+mixfn))) / (mixtp/(mixtp+mixfp) + mixtp/(mixtp+mixfn))
    #all using given equation for f1 score

    print("Unigram:", unif1)
    print("Bigram:", bif1)
    print("Mixed:", mixf1)

    return unif1, bif1, mixf1 #return all f1 score values

def significant_testing(a, b, c): #calculates signficance using alpha of .05
    alpha=0.05
    mean = (a + b + c) / 3
    total_sum_of_squares = sum([(x - mean) ** 2 for x in [a, b, c]])
    residual_sum_of_squares = sum([(x - mean) ** 2 for x in [a, b, c]])
    f_statistic = (total_sum_of_squares / 2) / (residual_sum_of_squares / 2)
    p_value = 1 - stats.f.cdf(f_statistic, 2, 2)
    return p_value, p_value < alpha #returns p value and if its significant or not

def mixedrun(): #runs each function needed for tasks
    lambdapath = "/Users/evankoenig/Desktop/Validation_Set"
    f1path = "/Users/evankoenig/Downloads/test.tsv"
    best_lambda = find_best_lambda(lambdapath)
    print("Best lambda value:", best_lambda)
    unigram_results, bigram_results, mixed_results = goldlabelresults(f1path, best_lambda)
    unif1, bif1, mixf1 = calculate_f1(unigram_results, bigram_results, mixed_results, f1path)
    p_value, significance = significant_testing(unif1, bif1, mixf1)
    if significance:
        print(f"p value: {p_value} yields significant results")
    else:
        print(f"p value: {p_value} yields insignificant results")

mixedrun()
