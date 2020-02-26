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
        CREATE TABLE Question (id SERIAL PRIMARY KEY,
                               question TEXT NOT NULL,
                               answer TEXT NOT NULL,
                               incorrect_1 TEXT NOT NULL,
                               incorrect_2 TEXT NOT NULL,
                               incorrect_3 TEXT NOT NULL);
        """)
        self.cursor.execute("""
        CREATE TABLE Subject (id TEXT PRIMARY KEY, name TEXT NOT NULL)
        """)
        self.cursor.execute("""
        CREATE TABLE Difficulty (difficulty INTEGER PRIMARY KEY, description TEXT NOT NULL)
        """)
        self.cursor.execute("""
        CREATE TABLE School (id SERIAL PRIMARY KEY, name TEXT NOT NULL, contact TEXT)
        """)

        self.cursor.execute("""
        CREATE TABLE Users (id SERIAL PRIMARY KEY, 
                            name TEXT NOT NULL,
                            passcode TEXT NOT NULL,
                            email TEXT NOT NULL UNIQUE,
                            school_id INTEGER NOT NULL,
        FOREIGN KEY(school_id) REFERENCES School (id) ON DELETE CASCADE
        )
        """)

        self.cursor.execute("""
        CREATE TABLE QuestionSubject (question_id INTEGER NOT NULL,
                                      subject_id TEXT NOT NULL,
        PRIMARY KEY(question_id, subject_id),
        FOREIGN KEY(question_id) REFERENCES Question (id) ON DELETE CASCADE,
        FOREIGN KEY(subject_id) REFERENCES Subject (id) ON DELETE CASCADE
        )
        """)
        
        self.cursor.execute("""
        CREATE TABLE QuestionDifficulty (question_id INTEGER UNIQUE NOT NULL,
                                         difficulty_id INTEGER NOT NULL,
        PRIMARY KEY(question_id, difficulty_id),
        FOREIGN KEY(question_id) REFERENCES Question (id) ON DELETE CASCADE,
        FOREIGN KEY(difficulty_id) REFERENCES Difficulty (difficulty) ON DELETE CASCADE
        )
        """)

        self.cursor.execute("""
        CREATE TABLE QuestionAnswered (user_id INTEGER NOT NULL,
                                       question_id INTEGER NOT NULL,
                                       correctly_answered BOOLEAN NOT NULL,
                                       actual_answered_value TEXT NOT NULL,
                                       time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY(user_id, question_id, time),
        FOREIGN KEY(user_id) REFERENCES Users (id) ON DELETE CASCADE,
        FOREIGN KEY(question_id) REFERENCES Question (id) ON DELETE CASCADE
        )
        """)

        self.conn.commit()

    
    def auth_user(self, email, passcode):
        self.cursor.execute(f"""
        SELECT * FROM Users WHERE email = '{email}' and passcode = '{passcode}'
        """)
        record = self.cursor.fetchone()
        print(f"auth user {record}")
        if record:
            return True
        else:
            return False


    #
    #   DATA FETCHING FUNCTIONS
    #

    def fetch_all_questions(self):
        self.cursor.execute("""
        SELECT * FROM Question JOIN QuestionDifficulty ON Question.id = QuestionDifficulty.question_id
        """)
        question = []
        for row in self.cursor:
            question.append(Question(question_id=row[0], question=row[1], answer=row[2], incorrect_1=row[3],
                                     incorrect_2=row[4], incorrect_3=row[5], difficulty_id=row[7]))

        return question


    def fetch_question(self, question_id):
        self.cursor.execute(f"""
        SELECT * FROM Question
        JOIN QuestionDifficulty ON Question.id = QuestionDifficulty.question_id
        JOIN QuestionSubject ON Question.id = QuestionSubject.question_id
        WHERE Question.id = {question_id}
        """)
        return self.cursor.fetchone()


    def fetch_user(self, email):
        self.cursor.execute(f"""
        SELECT * FROM Users WHERE email = '{email}'
        """)
        return self.cursor.fetchone()
    
    def fetch_user_name(self, user_id):
        self.cursor.execute(f"""
        SELECT name FROM Users WHERE id = '{user_id}'
        """)
        return self.cursor.fetchone()[0]

    def fetch_user_total_score(self, u_id):
        self.cursor.execute(f"""
        SELECT sum(questiondifficulty.difficulty_id) as TOTAL FROM QuestionAnswered
        JOIN QuestionDifficulty ON QuestionAnswered.question_id = QuestionDifficulty.question_id
        WHERE user_id = {u_id} AND QuestionAnswered.correctly_answered = true
        """)
        return self.cursor.fetchone()[0]

    def fetch_all_subjects(self):
        self.cursor.execute(f"""
        SELECT id, name FROM Subject
        """)
        return self.cursor.fetchall()

    def fetch_all_schools(self):
        self.cursor.execute(f"""
        SELECT id, name FROM School
        """)
        return self.cursor.fetchall()
    
    def fetch_subject_name(self, sub_id):
        self.cursor.execute(f"""
        SELECT name FROM Subject WHERE id = '{sub_id}'
        """)
        return self.cursor.fetchone()[0]
    
    def fetch_school_name(self, school_id):
        self.cursor.execute(f"""
        SELECT name FROM School WHERE id = {school_id}
        """)
        return self.cursor.fetchone()[0]

    def fetch_schools_users(self, school_id):
        self.cursor.execute(f"""
        SELECT * FROM Users WHERE school_id = {school_id}
        """)
        return self.cursor.fetchall()


    def fetch_leaderboard_school_subject(self, school_id, subject_id):
        self.cursor.execute(f"""
        SELECT QuestionAnswered.user_id, Users.name, sum(QuestionDifficulty.difficulty_id) FROM QuestionAnswered 
        JOIN QuestionDifficulty ON QuestionAnswered.question_id = QuestionDifficulty.question_id
        JOIN Users ON QuestionAnswered.user_id = Users.id
        JOIN School ON Users.school_id = School.id
        JOIN QuestionSubject ON QuestionAnswered.question_id = QuestionSubject.question_id
        WHERE QuestionAnswered.correctly_answered = true AND Users.school_id = {school_id} AND QuestionSubject.subject_id = '{subject_id}'
        GROUP BY QuestionAnswered.user_id, Users.name
        ORDER BY sum(QuestionDifficulty.difficulty_id) DESC
        """)
        records = []
        for i in self.cursor:
            records.append(i)
        return records

    def fetch_leaderboard_school(self, s_id):
        self.cursor.execute(f"""
        SELECT QuestionAnswered.user_id, Users.name, sum(QuestionDifficulty.difficulty_id) FROM QuestionAnswered 
        JOIN QuestionDifficulty ON QuestionAnswered.question_id = QuestionDifficulty.question_id
        JOIN Users ON QuestionAnswered.user_id = Users.id
        JOIN School on Users.school_id = School.id
        WHERE QuestionAnswered.correctly_answered = true AND Users.school_id = {s_id}
        GROUP BY QuestionAnswered.user_id, Users.name
        ORDER BY sum(QuestionDifficulty.difficulty_id) DESC
        """)

        records = []
        for i in self.cursor:
            records.append(i)
        return records

    def fetch_leaderboard_global(self):
        self.cursor.execute(f"""
        SELECT QuestionAnswered.user_id, Users.name, sum(QuestionDifficulty.difficulty_id), School.name FROM QuestionAnswered 
        JOIN QuestionDifficulty ON QuestionAnswered.question_id = QuestionDifficulty.question_id
        JOIN Users ON QuestionAnswered.user_id = Users.id
        JOIN School on Users.school_id = School.id
        WHERE QuestionAnswered.correctly_answered = true
        GROUP BY QuestionAnswered.user_id, Users.name, School.id
        ORDER BY sum(QuestionDifficulty.difficulty_id) DESC
        """)
        records = []
        for i in self.cursor:
            records.append(i)
        return records

    def fetch_user_question_history(self, user_id, question_id):
        self.cursor.execute(f"""
        SELECT * FROM QuestionAnswered
        WHERE user_id = {user_id} AND question_id = {question_id}
        ORDER BY time DESC
        """)
        return self.cursor.fetchall()

    def fetch_user_all_questions_history(self, user_id):
        self.cursor.execute(f"""
        SELECT * FROM QuestionAnswered
        WHERE user_id = {user_id}
        ORDER BY question_id, time
        """)
        return self.cursor.fetchall()

    # TODO: Needs to fetch all the users questions theyve answered. But multiple questions are repeated.. need to return each question_id only once.
    def fetch_user_all_questions_answered(self, user_id):
        self.cursor.execute(f"""
        SELECT * FROM QuestionAnswered
        WHERE user_id = {user_id}
        ORDER BY question_id, time
        """)
        return self.cursor.fetchall()


    #
    #   INSERTING FUNCTIONS
    #

    # todo; fix this function. DONE
    def add_question(self, question_class):
        question = question_class
        q_id = self.insert_question(question)
        question.question_id = q_id

        self.insert_question_difficulty(question)
        self.insert_question_subject(question)


    def insert_question(self, data):
        self.cursor.execute(f"""
        INSERT INTO Question (question, answer, incorrect_1, incorrect_2, incorrect_3)
        VALUES ('{data.question}', '{data.answer}', '{data.incorrect_1}', '{data.incorrect_2}', '{data.incorrect_3}')
        RETURNING id;
        """)
        q_id = self.cursor.fetchone()[0]
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
        """)
        # Removed this. Will store the result every time, and most these can be stored by date/time.
        # ON CONFLICT (user_id, question_id)
        # DO UPDATE SET correctly_answered = Excluded.correctly_answered, actual_answered_value = Excluded.actual_answered_value 

        self.conn.commit()
    

    #
    #   SETUP FUNCTIONS
    #
    
    def setup_dummy_data(self):
        self.insert_difficulty(Difficulty('Very Easy', 1))
        self.insert_difficulty(Difficulty('Easy', 2))
        self.insert_difficulty(Difficulty('Medium', 3))
        self.insert_difficulty(Difficulty('Hard', 4))
        self.insert_difficulty(Difficulty('Very Hard', 5))

        self.insert_subject(Subject('MATHS', 'Maths'))

        self.insert_school(School('Cowes Enterprise College'))
        self.insert_school(School('The International School for Spies'))
        

        self.add_question( Question("What is 10x10?", "100", "110", "1010", "120", "MATHS", "1") )
        self.add_question( Question("What is 25% of 8?", '2', '4', '3', '1', 'MATHS', '3') )
        self.add_question( Question("How many sides does a pentagon have?", '5', '4', '6', '7', 'MATHS', '1') )
        self.add_question( Question("What is 25+7", '32', '33', '31', '34', 'MATHS', '3') )
        self.add_question( Question("Whats the gradient of y=3x+4", '3', '3/4', '4/3', '4', 'MATHS', '5') )



        self.insert_user(User('Reece', '5678', 'reece@cowes.com', '1'))

    

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
    
    def set_it_up():

        print("Setting up")
        d.setup()

        print("Adding dummy data")
        d.setup_dummy_data()

        print("Done")

    # print(d.fetch_user_question_history(1, 1))
    # print(d.fetch_user_all_questions_history(1))
    # print(d.fetch_question(1))

    # d.insert_user(User('Sir', '0000', 'sir@cowes.com', '1'))