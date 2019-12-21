import psycopg2


class DatabaseManager:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()


    def close(self):
        self.conn.close()


    def drop_all(self):
        self.cursor.execute("""
        DROP TABLE IF EXISTS Question;
        """)
        self.cursor.execute("""
        DROP TABLE IF EXISTS Subject;
        """)
        self.cursor.execute("""
        DROP TABLE IF EXISTS QuestionSubject;
        """)
        self.cursor.execute("""
        DROP TABLE IF EXISTS Users;
        """)
        self.cursor.execute("""
        DROP TABLE IF EXISTS UserAnswered;
        """)
        self.cursor.execute("""
        DROP TABLE IF EXISTS School;
        """)
        self.cursor.execute("""
        DROP TABLE IF EXISTS UserSchool;
        """)
        self.conn.commit()


    def setup(self):
        self.drop_all()

        # todo: link tables
        # need to link to the submects table
        self.cursor.execute("""
        CREATE TABLE Question (id SERIAL PRIMARY KEY, question TEXT, answer TEXT, wrong_1 TEXT, wrong_2 TEXT, wrong_3 TEXT, subject TEXT, difficulty INTEGER);
        """)
        self.cursor.execute("""
        CREATE TABLE Subject (id SERIAL PRIMARY KEY, name TEXT)
        """)
        self.cursor.execute("""
        CREATE TABLE QuestionSubject (question_id INTEGER, subject_id INTEGER, PRIMARY KEY(question_id, subject_id))
        """)

        self.cursor.execute("""
        CREATE TABLE Users (id SERIAL PRIMARY KEY, username TEXT NOT NULL, passcode INTEGER NOT NULL)
        """)
        self.cursor.execute("""
        CREATE TABLE UserAnswered (user_id INTEGER, question_id INTEGER, correct BOOLEAN, PRIMARY KEY(user_id, question_id) )
        """)

        self.cursor.execute("""
        CREATE TABLE School (id SERIAL PRIMARY KEY, name TEXT)
        """)
        self.cursor.execute("""
        CREATE TABLE UserSchool (user_id INTEGER, school_id INTEGER, PRIMARY KEY(user_id, school_id) )
        """)

        self.conn.commit()

    
    def insert_question(self, data):
        self.cursor.execute(f"""
        INSERT INTO Question (question, answer, wrong_1, wrong_2, wrong_3, subject, difficulty)
        VALUES ('{data.question}', '{data.answer}', '{data.wrong_1}', '{data.wrong_2}', '{data.wrong_3}', '{data.subject}', '{data.difficulty}')
        """)
        self.conn.commit()

    
    def fetch_all(self):
        self.cursor.execute("""
        SELECT * FROM Question
        """)
        question = []
        for row in self.cursor:
            question.append(Question(q_id=row[0], question=row[1], answer=row[2], wrong_1=row[3],
                                     wrong_2=row[4], wrong_3=row[5], subject=row[6], difficulty=row[7]))
        return question


class Question:
    def __init__(self, question, answer, wrong_1, wrong_2, wrong_3, subject, difficulty, q_id=None):
        self.id = q_id
        self.question = question
        self.answer = answer
        self.wrong_1 = wrong_1
        self.wrong_2 = wrong_2
        self.wrong_3 = wrong_3
        self.subject = subject
        self.difficulty = difficulty


def postgres_example():
    conn = psycopg2.connect("dbname='database1' user=postgres password='pass' host='localhost' port='5432'")
    db = DatabaseManager(conn)

    db.drop_all()
    db.setup()

    q1 = Question('What is 12x12?', '144', '121', '141', '240', 'Maths', 2)
    q2 = Question('What does CPU stand for?', 'Central Processing Unit', 'Central Power Unit', 'Computing Power Unit', 'Computer Programming Unit', 'Comp Sci', 1)
    q3 = Question('How do you find the gradient of a polynomial equation?', 'Differentiate', 'Integrate', 'Simultaneous Equations', 'Square Root', 'Maths', 3)

    q4 = Question('What colour is grass?', 'Green', 'Blue', 'Red', 'Pink', 'Geography', 1)
    q5 = Question('Translate "Hello" into French', 'Bonjour', 'Hola', 'Je Suis', 'Pomme', 'French', 2)
    q6 = Question('Who wrote "A Christmas Carol"?', 'Charles Dickens', 'Thomas Hardy', 'William Shakespeare', 'J. K. Rowling', 'English', 3)


    db.insert_question(q4)
    db.insert_question(q5)
    db.insert_question(q6)

    db.insert_question(q1)
    db.insert_question(q2)
    db.insert_question(q3)

    results = db.fetch_all()
    print(results[0].question, results[0].answer)


if __name__ == "__main__":
    postgres_example()