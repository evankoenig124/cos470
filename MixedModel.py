from BigramModel import bigramrun
from UnigramModel import unigramrun
import os

def find_best_lambda(directory_path):
    highest_correct_predictions = 0
    best_lambda_value = 0
        
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
                    
                    if min(combined_results, key=combined_results.get) == actual_genre:
                        current_correct_predictions += 1

            # Check if there are more correct predictions than before
        if highest_correct_predictions < current_correct_predictions:
            highest_correct_predictions = current_correct_predictions
            best_lambda_value = lambda_value
                
    return best_lambda_value

def main():
    path = "/Users/evankoenig/Desktop/Validation_Set"

    print(find_best_lambda(path))
main()