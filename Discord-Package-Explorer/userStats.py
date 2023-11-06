import os
import csv
import string
from collections import Counter

# Function to extract words from a text
def extract_words(text):
    words = text.split()
    return [word.strip(string.punctuation) for word in words]

# Function to find the top N words in a list while excluding specific words
def find_top_words_exclude(word_list, exclude_words, n=10):
    word_counter = Counter(word for word in word_list if word not in exclude_words)
    return word_counter.most_common(n)

# Function to process CSV files and find top words
def topwords(directory, exclude_words, n=10):
    # Initialize a list to store words from all CSV files
    all_words = []

    # Iterate through all files in the directory and its subdirectories
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as csv_file:
                    csv_reader = csv.reader(csv_file)
                    for row in csv_reader:
                        for cell in row:
                            words = extract_words(cell)
                            all_words.extend(word for word in words if word not in exclude_words)

    # Find the top N most used words across all CSV files while excluding specific words
    top_words = find_top_words_exclude(all_words, exclude_words, n)

    # Print the results
    return top_words

# Example usage:
if __name__ == "__main__":
    directory = r'C:\Users\alain\Desktop\package\messages'
    exclude_words = ["UPWAKE", ""]
    n = 10
    top_words = topwords(directory, exclude_words, n)
    print(top_words)
