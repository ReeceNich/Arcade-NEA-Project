import psycopg2


class DatabaseManager:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()


    def close(self):
        self.conn.close()


    def drop_all(self):
        self.cursor.execute("""
        DROP SCHEMA public CASCADE;
        CREATE SCHEMA public;

        GRANT ALL ON SCHEMA public TO postgres;
        GRANT ALL ON SCHEMA public TO public;
        """)

        self.conn.commit()


    def setup(self):
        self.drop_all()

        self.cursor.execute("""
        CREATE TABLE Question (id SERIAL PRIMARY KEY, question TEXT NOT NULL, answer TEXT NOT NULL, incorrect_1 TEXT NOT NULL, incorrect_2 TEXT NOT NULL, incorrect_3 TEXT NOT NULL);
        """)
        self.cursor.execute("""
        CREATE TABLE Subject (id TEXT PRIMARY KEY, name TEXT NOT NULL)
        """)
        self.cursor.execute("""
        CREATE TABLE Difficulty (difficulty INTEGER PRIMARY KEY, description TEXT NOT NULL)
        """)
        self.cursor.execute("""
        CREATE TABLE School (id SERIAL PRIMARY KEY, name TEXT NOT NULL)
        """)

        self.cursor.execute("""
        CREATE TABLE Users (id SERIAL PRIMARY KEY, name TEXT NOT NULL, passcode TEXT NOT NULL, email TEXT NOT NULL UNIQUE, school_id INTEGER NOT NULL,
        FOREIGN KEY(school_id) REFERENCES School (id) ON DELETE CASCADE
        )
        """)

        self.cursor.execute("""
        CREATE TABLE QuestionSubject (question_id INTEGER NOT NULL, subject_id TEXT NOT NULL,
        PRIMARY KEY(question_id, subject_id),
        FOREIGN KEY(question_id) REFERENCES Question (id) ON DELETE CASCADE,
        FOREIGN KEY(subject_id) REFERENCES Subject (id) ON DELETE CASCADE
        )
        """)
        
        self.cursor.execute("""
        CREATE TABLE QuestionDifficulty (question_id INTEGER UNIQUE NOT NULL, difficulty_id INTEGER NOT NULL,
        PRIMARY KEY(question_id, difficulty_id),
        FOREIGN KEY(question_id) REFERENCES Question (id) ON DELETE CASCADE,
        FOREIGN KEY(difficulty_id) REFERENCES Difficulty (difficulty) ON DELETE CASCADE
        )
        """)

        self.cursor.execute("""
        CREATE TABLE QuestionAnswered (user_id INTEGER NOT NULL, question_id INTEGER NOT NULL, correctly_answered BOOLEAN NOT NULL, actual_answered_value TEXT NOT NULL,
        PRIMARY KEY(user_id, question_id),
        FOREIGN KEY(user_id) REFERENCES Users (id) ON DELETE CASCADE,
        FOREIGN KEY(question_id) REFERENCES Question (id) ON DELETE CASCADE
        )
        """)
        

        self.conn.commit()

    
    def fetch_all_questions(self):
        self.cursor.execute("""
        SELECT * FROM Question JOIN QuestionDifficulty ON Question.id = QuestionDifficulty.question_id
        """)
        question = []
        for row in self.cursor:
            question.append(Question(question_id=row[0], question=row[1], answer=row[2], incorrect_1=row[3],
                                     incorrect_2=row[4], incorrect_3=row[5], difficulty_id=row[7]))
        return question


    def insert_question(self, data):
        self.cursor.execute(f"""
        INSERT INTO Question (question, answer, incorrect_1, incorrect_2, incorrect_3)
        VALUES ('{data.question}', '{data.answer}', '{data.incorrect_1}', '{data.incorrect_2}', '{data.incorrect_3}')
        RETURNING id;
        """)
        q_id = self.cursor.fetchone()[0]
        print("THE ID IS:", q_id)
        self.conn.commit()
        return q_id
    
    def insert_question_difficulty(self, data):
        self.cursor.execute(f"""
        INSERT INTO QuestionDifficulty (question_id, difficulty_id)
        VALUES ('{data.question_id}', '{data.difficulty_id}')
        """)
        self.conn.commit()

    def insert_question_subject(self, data):
        self.cursor.execute(f"""
        INSERT INTO QuestionSubject (question_id, subject_id)
        VALUES ('{data.question_id}', '{data.subject_id}')
        """)
        self.conn.commit()
    
    def insert_subject(self, data):
        self.cursor.execute(f"""
        INSERT INTO Subject (id, name)
        VALUES ('{data.subject_id}', '{data.name}')
        """)
        self.conn.commit()

    def insert_difficulty(self, data):
        self.cursor.execute(f"""
        INSERT INTO Difficulty (difficulty, description)
        VALUES ('{data.difficulty_id}', '{data.description}')
        """)
        self.conn.commit()

    def insert_school(self, data):
        self.cursor.execute(f"""
        INSERT INTO School (name)
        VALUES ('{data.name}')
        """)
        self.conn.commit()

    def insert_user(self, data):
        self.cursor.execute(f"""
        INSERT INTO Question (question, answer, incorrect_1, incorrect_2, incorrect_3)
        VALUES ('{data.question}', '{data.answer}', '{data.incorrect_1}', '{data.incorrect_2}', '{data.incorrect_3}')
        """)
        self.conn.commit()
    

class School:
    def __init__(self, question, answer, question_id=None):
        self.id = question_id
        self.question = question
        self.answer = answer

class Question:
    def __init__(self, question, answer, incorrect_1, incorrect_2, incorrect_3, subject_id=None, difficulty_id=None, question_id=None):
        self.question_id = question_id
        self.question = question
        self.answer = answer
        self.incorrect_1 = incorrect_1
        self.incorrect_2 = incorrect_2
        self.incorrect_3 = incorrect_3
        self.subject_id = subject_id
        self.difficulty_id = difficulty_id

class Difficulty:
    def __init__(self, description, difficulty_id=None):
        self.difficulty_id = difficulty_id
        self.description = description

class Subject:
    def __init__(self, subject_id, name):
        self.subject_id = subject_id
        self.name = name


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


def drop_all():
    conn = psycopg2.connect("dbname='database1' user=postgres password='pass' host='localhost' port='5432'")
    db = DatabaseManager(conn)
    db.drop_all()

if __name__ == "__main__":
    create_dummy_database()
