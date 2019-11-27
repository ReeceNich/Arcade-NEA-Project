import psycopg2


class DB:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()


    def close(self):
        self.conn.close()


    def drop_all(self):
        self.cursor.execute("""
        DROP TABLE IF EXISTS Questions;
        """)
        self.cursor.execute("""
        DROP TABLE IF EXISTS Users;
        """)
        self.conn.commit()


    def setup(self):
        self.drop_all()

        self.cursor.execute("""
        CREATE TABLE Questions (id SERIAL PRIMARY KEY, question TEXT, answer TEXT, wrong_1 TEXT, wrong_2 TEXT, wrong_3 TEXT, subject TEXT, difficulty INTEGER);
        """)
        self.cursor.execute("""
        CREATE TABLE Users (id SERIAL PRIMARY KEY, username TEXT NOT NULL, passcode INTEGER NOT NULL)
        """)
        
        self.conn.commit()

    
    def insert_question(self, data):
        self.cursor.execute(f"""
        INSERT INTO Questions (question, answer, wrong_1, wrong_2, wrong_3, subject, difficulty)
        VALUES ('{data.question}', '{data.answer}', '{data.wrong_1}', '{data.wrong_2}', '{data.wrong_3}', '{data.subject}', '{data.difficulty}')
        """)
        self.conn.commit()

    
    def fetch_all(self):
        self.cursor.execute("""
        SELECT * FROM Questions
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
    db = DB(conn)

    # db.setup()
    # print("setup")

    # q1 = Question('What is 12x12?', '144', '121', '141', '240', 'Maths', 2)
    # q2 = Question('What does CPU stand for?', 'Central Processing Unit', 'Central Power Unit', 'Computing Power Unit', 'Computer Programming Unit', 'Comp Sci', 1)
    # q3 = Question('How do you find the gradient of a polynomial equation?', 'Differentiate', 'Integrate', 'Simultaneous Equations', 'Square Root', 'Maths', 3)
    # db.insert_question(q1)
    # db.insert_question(q2)
    # db.insert_question(q3)

    results = db.fetch_all()
    print(results[0].question, results[0].answer)


if __name__ == "__main__":
    postgres_example()