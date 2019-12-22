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
        CREATE TABLE Question (id SERIAL PRIMARY KEY, question TEXT, answer TEXT, incorrect_1 TEXT, incorrect_2 TEXT, incorrect_3 TEXT);
        """)
        self.cursor.execute("""
        CREATE TABLE Subject (id SERIAL PRIMARY KEY, name TEXT)
        """)
        self.cursor.execute("""
        CREATE TABLE QuestionSubject (question_id INTEGER, subject_id INTEGER, PRIMARY KEY(question_id, subject_id))
        """)
        self.cursor.execute("""
        CREATE TABLE Difficulty (difficulty INTEGER PRIMARY KEY, description TEXT)
        """)
        self.cursor.execute("""
        CREATE TABLE QuestionDifficulty (question_id INTEGER, difficulty_id INTEGER, PRIMARY KEY(question_id, difficulty_id))
        """)

        self.cursor.execute("""
        CREATE TABLE QuestionAnswered (user_id INTEGER, question_id INTEGER, correctly_answered BOOLEAN, actual_answered_value TEXT, PRIMARY KEY(user_id, question_id) )
        """)

        self.cursor.execute("""
        CREATE TABLE Users (id SERIAL PRIMARY KEY, username TEXT NOT NULL, passcode INTEGER NOT NULL, email TEXT, school_id INTEGER)
        """)
        self.cursor.execute("""
        CREATE TABLE School (id SERIAL PRIMARY KEY, name TEXT)
        """)
        

        self.conn.commit()

    
    def insert_question(self, data):
        self.cursor.execute(f"""
        INSERT INTO Question (question, answer, incorrect_1, incorrect_2, incorrect_3)
        VALUES ('{data.question}', '{data.answer}', '{data.incorrect_1}', '{data.incorrect_2}', '{data.incorrect_3}')
        """)
        self.conn.commit()

    
    def fetch_all(self):
        self.cursor.execute("""
        SELECT * FROM Question
        """)
        question = []
        for row in self.cursor:
            question.append(Question(q_id=row[0], question=row[1], answer=row[2], incorrect_1=row[3],
                                     incorrect_2=row[4], incorrect_3=row[5]))
        return question


class Question:
    def __init__(self, question, answer, incorrect_1, incorrect_2, incorrect_3, q_id=None):
        self.id = q_id
        self.question = question
        self.answer = answer
        self.incorrect_1 = incorrect_1
        self.incorrect_2 = incorrect_2
        self.incorrect_3 = incorrect_3


def create_dummy_database():
    conn = psycopg2.connect("dbname='database1' user=postgres password='pass' host='localhost' port='5432'")
    db = DatabaseManager(conn)

    db.drop_all()
    db.setup()

    # q1 = Question('What is 12x12?', '144', '121', '141', '240', 'Maths', 2)
    # q2 = Question('What does CPU stand for?', 'Central Processing Unit', 'Central Power Unit', 'Computing Power Unit', 'Computer Programming Unit', 'Comp Sci', 1)
    # q3 = Question('How do you find the gradient of a polynomial equation?', 'Differentiate', 'Integrate', 'Simultaneous Equations', 'Square Root', 'Maths', 3)

    # q4 = Question('What colour is grass?', 'Green', 'Blue', 'Red', 'Pink', 'Geography', 1)
    # q5 = Question('Translate "Hello" into French', 'Bonjour', 'Hola', 'Je Suis', 'Pomme', 'French', 2)
    # q6 = Question('Who wrote "A Christmas Carol"?', 'Charles Dickens', 'Thomas Hardy', 'William Shakespeare', 'J. K. Rowling', 'English', 3)


    # db.insert_question(q4)
    # db.insert_question(q5)
    # db.insert_question(q6)

    # db.insert_question(q1)
    # db.insert_question(q2)
    # db.insert_question(q3)

    # results = db.fetch_all()
    # print(results[0].question, results[0].answer)
    
    print("Created dummy database!")


def drop_all():
        conn = psycopg2.connect("dbname='database1' user=postgres password='pass' host='localhost' port='5432'")
        db = DatabaseManager(conn)
        db.drop_all()

if __name__ == "__main__":
    create_dummy_database()
