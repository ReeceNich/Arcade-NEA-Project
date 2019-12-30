from database_manager import *

def create_dummy_database():
    conn = psycopg2.connect("dbname='database1' user=postgres password='pass' host='localhost' port='5432'")
    db = DatabaseManager(conn)

    db.drop_all()
    db.setup()

    # q1 = Question('What is 12x12?', '144', '121', '141', '240', 'Maths', 2)
    # q2 = Question('What does CPU stand for?', 'Central Processing Unit', 'Central Power Unit', 'Computing Power Unit', 'Computer Programming Unit', 'Comp Sci', 1)
    # q3 = Question('How do you find the gradient of a polynomial equation?', 'Differentiate', 'Integrate', 'Simultaneous Equations', 'Square Root', 'Maths', 3)

    # db.insert_question(q1)
    # db.insert_question(q2)
    # db.insert_question(q3)

    # results = db.fetch_all()
    # print(results[0].question, results[0].answer)


    add_dummy_difficulties(db)
    add_dummy_subjects(db)
    add_dummy_question(db)
    
    print("Created dummy database!")

def add_dummy_difficulties(db):
    difficulties = [Difficulty("Very Easy", 1), Difficulty("Easy", 2), Difficulty("Medium", 3), Difficulty("Hard", 4), Difficulty("Very Hard", 5)]
    for i in difficulties:
        db.insert_difficulty(i)

def add_dummy_subjects(db):
    subjects = [Subject("MATHS", "Maths"),
                Subject("COMP_SCI", "Computer Science"),
                Subject("GEOGRAPHY", "Geography"),
                Subject("FRENCH", "French"),
                Subject("ENG_LIT", "English Literature"),
                Subject("ENG_LANG", "English Language")]
    
    for s in subjects:
        db.insert_subject(s)

def add_dummy_question(db):
    questions = [Question('What is 12x12?', '144', '121', '141', '240', subject_id="MATHS", difficulty_id=2),
                 Question('What colour is grass?', 'Green', 'Blue', 'Red', 'Pink', subject_id="GEOGRAPHY", difficulty_id=1),
                 Question('Translate "Hello" into French', 'Bonjour', 'Hola', 'Je Suis', 'Pomme', subject_id="FRENCH", difficulty_id=1),
                 Question('Who wrote "A Christmas Carol"?', 'Charles Dickens', 'Thomas Hardy', 'William Shakespeare', 'J. K. Rowling', subject_id="ENG_LIT", difficulty_id=3)]

    for q in questions:
        q.question_id = db.insert_question(q)
        db.insert_question_difficulty(q)
        db.insert_question_subject(q)


def drop_everything():
    conn = psycopg2.connect("dbname='database1' user=postgres password='pass' host='localhost' port='5432'")
    db = DatabaseManager(conn)
    db.drop_all()


def insert_question(db):
    pass

def main():
    print("""
    Welcome t
    """)
    choice = input("What do you want to do? ")
    if choice == 

if __name__ == "__main__":
    create_dummy_database()