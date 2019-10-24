"""
Opens the CSV file of all the questions and returns a list with items as dictionaries containing id, question, answer, wrong answers (1 to 3) and difficulty.
"""
import csv
import sqlite3

def read_csv_to_dictionary(filename):
    # open the csv file
    with open(filename, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        line_count = 0
        all_data = []

        # for each row, get the columns and append to a dictionary.
        for row in csv_reader:
            # gets the names of the columns in the csv file.
            if line_count == 0:
                print(f"The column names are {', '.join(row)}.")
                line_count += 1
            else:
                row_data = {"id": row[0],
                            "question": row[1],
                            "correct_answer": row[2],
                            "wrong_answer_1": row[3],
                            "wrong_answer_2": row[4],
                            "wrong_answer_3": row[5],
                            "difficulty": row[6]}
                all_data.append(row_data)
                # print(f"ID: {row['id']}, Q: {row['question']}, A1: {row['correct_answer']}, A2: {row['wrong_answer_1']}, A3: {row['wrong_answer_2']}, A4: {row['wrong_answer_3']}, D: {row['difficulty']}/5.")
                line_count += 1
        
        return all_data


def sql_to_csv(sql_filename, csv_filename):
    try:
        # open the database
        with open(csv_filename, mode='w') as csv_writer:
            # connect to the database
            connection = sqlite3.connect(sql_filename)
            cursor = connection.cursor()

            for row in cursor.execute('SELECT * FROM questions'):
                csv_writer.write(row)
        
        return True
    except:
        raise


if __name__ == "__main__":
    d = read_csv_to_dictionary('questions.csv')
    for row in d:
        print(row)
    

    sql_to_csv("questions.csv", "testing_questions.csv")