"""
Opens the CSV file of all the questions and returns a list with items as dictionaries containing id, question, answers and difficulty.
"""
import csv

def read_csv(filename):
    # open the csv file
    with open(filename, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        line_count = 0
        data = []

        for row in csv_reader:
            if line_count == 0:
                print(f"The column names are {', '.join(row)}.")
                columns = row
                line_count += 1

            else:
                #print(f"ID: {row['id']}, Q: {row['question']}, A1: {row['correct_answer']}, A2: {row['wrong_answer_1']}, A3: {row['wrong_answer_2']}, A4: {row['wrong_answer_3']}, D: {row['difficulty']}/10.")
                temp_dict = {columns[0]: row[0],
                            columns[1]: row[1],
                            columns[2]: row[2],
                            columns[3]: row[3],
                            columns[4]: row[4],
                            columns[5]: row[5],
                            columns[6]: row[6]}
                data.append(temp_dict)
                line_count += 1

        print(f"Total lines = {line_count}.")
        return data


if __name__ == "__main__":
    d = read_csv('questions.txt')
    for row in d:
        print(row)
    