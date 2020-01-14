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

    def fetch_user(self, email):
        self.cursor.execute(f"""
        SELECT * FROM Users WHERE email = '{email}'
        """)
        return self.cursor.fetchone()

    def fetch_user_total_score(self, u_id):
        self.cursor.execute(f"""
        SELECT sum(questiondifficulty.difficulty_id) as TOTAL FROM QuestionAnswered
        JOIN QuestionDifficulty ON QuestionAnswered.question_id = QuestionDifficulty.question_id
        WHERE user_id = {u_id} AND QuestionAnswered.correctly_answered = true
        """)
        return self.cursor.fetchone()[0]

    def fetch_leaderboard_school(self, u_id):
        s_id = 1

        self.cursor.execute(f"""
        SELECT QuestionAnswered.user_id, Users.name, sum(QuestionDifficulty.difficulty_id) FROM QuestionAnswered 
        JOIN QuestionDifficulty ON QuestionAnswered.question_id = QuestionDifficulty.question_id
        JOIN Users ON QuestionAnswered.user_id = Users.id
        JOIN School on Users.school_id = School.id
        WHERE QuestionAnswered.correctly_answered = true AND Users.school_id = {s_id}
        GROUP BY QuestionAnswered.user_id, Users.name
        """)

        # this fetches every users CORRECTLY ANSWERED entries, along with their school and user info.
        """
        SELECT * FROM QuestionAnswered 
        JOIN QuestionDifficulty ON QuestionAnswered.question_id = QuestionDifficulty.question_id
        JOIN Users ON QuestionAnswered.user_id = Users.id
        JOIN School on Users.school_id = School.id
        WHERE QuestionAnswered.correctly_answered = true;
        """

        # returns just user ID and sum of the total correctly answered.
        """
        SELECT QuestionAnswered.user_id, sum(QuestionDifficulty.difficulty_id) FROM QuestionAnswered 
        JOIN QuestionDifficulty ON QuestionAnswered.question_id = QuestionDifficulty.question_id
        JOIN Users ON QuestionAnswered.user_id = Users.id
        JOIN School on Users.school_id = School.id
        WHERE QuestionAnswered.correctly_answered = true
        GROUP BY QuestionAnswered.user_id;
        """
        records = []
        for i in self.cursor:
            records.append(i)
        return records


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
        RETURNING id;
        """)
        s_id = self.cursor.fetchone()[0]
        self.conn.commit()
        return s_id

    def insert_user(self, data):
        self.cursor.execute(f"""
        INSERT INTO Users (name, passcode, email, school_id)
        VALUES ('{data.name}', '{data.passcode}', '{data.email}', '{data.school_id}')
        RETURNING id;
        """)
        u_id = self.cursor.fetchone()[0]
        self.conn.commit()
        return u_id

    def insert_question_answered(self, data):
        self.cursor.execute(f"""
        INSERT INTO QuestionAnswered (user_id, question_id, correctly_answered, actual_answered_value)
        VALUES ({data.user_id}, {data.question_id}, {data.correctly_answered}, '{data.actual_answered_value}')
        ON CONFLICT (user_id, question_id)
        DO UPDATE SET correctly_answered = Excluded.correctly_answered, actual_answered_value = Excluded.actual_answered_value 
        """)
        self.conn.commit()
    

class School:
    def __init__(self, name, school_id=None):
        self.id = school_id
        self.name = name

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

class User:
    def __init__(self, name, passcode, email, school_id, user_id=None):
        self.id = user_id
        self.name = name
        self.passcode = passcode
        self.email = email
        self.school_id = school_id

class QuestionAnswered:
    def __init__(self, user_id, question_id, correctly_answered, actual_answered_value):
        self.user_id = user_id
        self.question_id = question_id
        self.correctly_answered = correctly_answered
        self.actual_answered_value = actual_answered_value


if __name__ == "__main__":
    d = DatabaseManager(psycopg2.connect("dbname='database1' user=postgres password='pass' host='localhost' port='5432'"))
    # print(d.fetch_user_total_score(2))
    # print(d.fetch_user_total_score(3))
    records = d.fetch_leaderboard_school(2)
    print("ID  |  Name  |  Score")
    for i in records:
        print("{:<7d}{:<9s}{:<5d}".format(i[0], i[1], i[2]))