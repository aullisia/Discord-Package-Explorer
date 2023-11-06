import os
import csv

#csv word search
def find_csv_files(folder_path, search_text):
    filelist = []
    total_count = 0  # Initialize a variable to store the total count
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.csv'):
                csv_file_path = os.path.join(root, file)
                count = count_text_in_csv(csv_file_path, search_text)
                if count > 0:
                    # Append to the filelist, not file
                    filelist.append([csv_file_path, count])
                total_count += count  # Update the total count

    # Sort the filelist based on count (from big to small)
    filelist.sort(key=lambda x: x[1], reverse=True)

    return total_count, filelist


def count_text_in_csv(csv_file, search_text):
    count = 0
    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            count += sum(1 for cell in row if search_text in cell)
    return count

def start(word, path):
    folder_path = path
    search_text = str(word)

    #print(folder_path)

    total_count, file_list = find_csv_files(folder_path, search_text)

    return total_count, file_list