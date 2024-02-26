from BigramModel import bigramrun
from UnigramModel import unigramrun
import os
import csv

def find_best_lambda(directory_path):
    highest_correct_predictions = 0
    best_lambda_value = 0
    best_lambda_results = {}
        
    for i in range(11):
        lambda_value = i / 10.0
        current_correct_predictions = 0
        
        for file in os.listdir(directory_path):  # For each song in the validation set

            if file.endswith('.txt'):
                print("newfile")
                with open(os.path.join(directory_path, file), 'r') as file:
                    actual_genre = file.readline()
                    actual_genre = actual_genre.strip()

                    text = file.read()  # Read the rest of the text
                    unigram_results = unigramrun(text)
                    print("uni")
                    bigram_results = bigramrun(text)
                    print("bi")

                    combined_results = {}
                    for genre in unigram_results:
                        combined_probability = (lambda_value * unigram_results[genre]) + ((1 - lambda_value) * bigram_results[genre])
                        combined_results[genre] = combined_probability
                    
                    print(combined_results)
                    if min(combined_results, key=combined_results.get) == actual_genre:
                        current_correct_predictions += 1

            # Check if there are more correct predictions than before
        if highest_correct_predictions < current_correct_predictions:
            highest_correct_predictions = current_correct_predictions
            best_lambda_value = lambda_value
                
    return best_lambda_value

def calculate_mixed(path, lambda_value):
    unigram_results = {}
    bigram_results = {}
    mixed_results = {}
    i = 0

    with open(path, 'r', newline='') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        for song in reader:
            unigram_line = unigramrun(song[1])
            bigram_line = bigramrun(song[1])
            mixed_line = {}
            for genre in unigram_line:
                combined_probability = (lambda_value * unigram_line[genre]) + ((1 - lambda_value) * bigram_line[genre])
                mixed_line[genre] = combined_probability
            unigram_results[i] = unigram_line
            bigram_results[i] = bigram_line
            mixed_results[i] = mixed_line
            i += 1
    
    return unigram_results, bigram_results, mixed_results

def calculate_f1(unigram, bigram, mixed, path):
    f1results = {}

    unitp = 0
    unifp = 0
    unifn = 0

    bitp = 0
    bifp = 0
    bifn = 0

    mixtp = 0
    mixfp = 0
    mixfn = 0

    with open(path, 'r', newline='') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        for song in reader:
            for id in unigram:
                # Unigram
                if min(unigram[id], key=unigram[id].get) == song[2]:
                    unitp += 1
                else:
                    if song[2] in unigram[id].keys():
                        unifn += 1
                    else:
                        unifp += 1
                
                # Bigram
                if min(bigram[id], key=bigram[id].get) == song[2]:
                    bitp += 1
                else:
                    if song[2] in bigram[id].keys():
                        bifn += 1
                    else:
                        bifp += 1
                
                # Mixed
                if min(mixed[id], key=mixed[id].get) == song[2]:
                    mixtp += 1
                else:
                    if song[2] in mixed[id].keys():
                        mixfn += 1
                    else:
                        mixfp += 1  

    unif1 = (2*(unitp/(unitp+unifp))*(unitp/(unitp+unifn))) / (unitp/(unitp+unifp) + unitp/(unitp+unifn))
    bif1 = (2*(bitp/(bitp+bifp))*(bitp/(bitp+bifn))) / (bitp/(bitp+bifp) + bitp/(bitp+bifn))
    mixf1 = (2*(mixtp/(mixtp+mixfp))*(mixtp/(mixtp+mixfn))) / (mixtp/(mixtp+mixfp) + mixtp/(mixtp+mixfn))

    print("Unigram:", unif1)
    print("Bigram:", bif1)
    print("Mixed:", mixf1)

    return unif1, bif1, mixf1

def sigtest(unif1, bif1, mixf1):
    print("done")

def mixedrun():
    lambdapath = "/Users/evankoenig/Desktop/Validation_Set"
    f1path = "/Users/evankoenig/Downloads/test.tsv"
    #best_lambda = find_best_lambda(lambdapath)
    best_lambda = 0.4
    unigram_results, bigram_results, mixed_results = calculate_mixed(f1path, best_lambda)
    unif1, bif1, mixf1 = calculate_f1(unigram_results, bigram_results, mixed_results, f1path)
    sigtest(unif1, bif1, mixf1)

mixedrun()

#try f1 score first, .4 is best lambda, 