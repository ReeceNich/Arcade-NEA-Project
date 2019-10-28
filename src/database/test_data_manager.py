from data_manager import read_csv_to_dictionary, database_to_csv,\
    csv_to_database, create_database


def test_read_csv_to_dictionary(csv_filename):
    d = read_csv_to_dictionary(csv_filename)
    for row in d:
        print(row)


def test_create_database(database_filename):
    create_database("questions.db")

def test_database_to_csv(database_filename, csv_filename):
    database_to_csv(database_filename, csv_filename)

def test_csv_to_database(csv_filename, database_filename):
    csv_to_database(csv_filename, database_filename)


if __name__ == "__main__":
    # test_read_csv_to_dictionary('questions.csv')
    # create_database("questions.db")
    test_csv_to_database("questions.csv", "questions.db")