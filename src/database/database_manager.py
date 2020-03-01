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
        CREATE TABLE School (id SERIAL,
                             name TEXT NOT NULL,
                             contact TEXT,
                             
                             PRIMARY KEY (id)
                             )
        """)

        self.cursor.execute("""
        CREATE TABLE Difficulty (id INTEGER UNIQUE NOT NULL,
                                 name TEXT NOT NULL,

                                 PRIMARY KEY (id)
                                 )
        """)

        self.cursor.execute("""
        CREATE TABLE Subject (id TEXT UNIQUE NOT NULL,
                              name TEXT NOT NULL,

                              PRIMARY KEY (id)
                              )
        """)

        self.cursor.execute("""
        CREATE TABLE YearGroup (id INTEGER UNIQUE NOT NULL,
                                name TEXT UNIQUE NOT NULL,

                                PRIMARY KEY (id)
                                )
        """)

        self.cursor.execute("""
        CREATE TABLE Topic (id TEXT NOT NULL,
                            name TEXT NOT NULL,
                            subject_id TEXT NOT NULL,

                            UNIQUE (id, subject_id),
                            PRIMARY KEY (id, subject_id),
                            FOREIGN KEY(subject_id) REFERENCES Subject (id) ON DELETE CASCADE
                            )
        """)

        self.cursor.execute("""
        CREATE TABLE Teacher (id SERIAL,
                              username TEXT NOT NULL,
                              passcode TEXT NOT NULL,
                              school_id INTEGER NOT NULL,

                              UNIQUE (username, school_id),
                              
                              PRIMARY KEY (id),
                              FOREIGN KEY(school_id) REFERENCES School (id) ON DELETE CASCADE
                              )
        """)

        self.cursor.execute("""
        CREATE TABLE Users (id SERIAL,
                            name TEXT NOT NULL,
                            username TEXT NOT NULL,
                            passcode TEXT NOT NULL,
                            nickname TEXT,
                            year_group_id INTEGER NOT NULL,
                            school_id INTEGER NOT NULL,

                            UNIQUE (username, school_id),

                            PRIMARY KEY (id),
                            FOREIGN KEY(school_id) REFERENCES School (id) ON DELETE CASCADE,
                            FOREIGN KEY(year_group_id) REFERENCES YearGroup (id) ON DELETE CASCADE
                            )
        """)

        self.cursor.execute("""
        CREATE TABLE Question (id SERIAL,
                               question TEXT NOT NULL,
                               difficulty_id INTEGER NOT NULL,
                               topic_id TEXT NOT NULL,
                               subject_id TEXT NOT NULL,

                               PRIMARY KEY (id),
                               FOREIGN KEY(difficulty_id) REFERENCES Difficulty (id) ON DELETE CASCADE,
                               FOREIGN KEY(topic_id, subject_id) REFERENCES Topic (id, subject_id) ON DELETE CASCADE,
                               FOREIGN KEY(subject_id) REFERENCES Subject (id) ON DELETE CASCADE
                               )
        """)

        self.cursor.execute("""
        CREATE TABLE Answer (question_id INTEGER NOT NULL,
                             answer_id INTEGER NOT NULL,
                             correct BOOLEAN NOT NULL,
                             answer TEXT NOT NULL,
                             
                             PRIMARY KEY (question_id, answer_id),
                             FOREIGN KEY(question_id) REFERENCES Question (id) ON DELETE CASCADE
                             )
        """)

        self.cursor.execute("""
        CREATE TABLE QuestionAnswered (user_id INTEGER NOT NULL,
                                       question_id INTEGER NOT NULL,
                                       answer_id INTEGER NOT NULL,
                                       time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                                       
                                       PRIMARY KEY (user_id, question_id, answer_id, time),
                                       FOREIGN KEY(user_id) REFERENCES Users (id) ON DELETE CASCADE,
                                       FOREIGN KEY(question_id) REFERENCES Question (id) ON DELETE CASCADE
                                       )
        """)


        self.conn.commit()

    
    # if a result is returned from the database, it must mean all the fields match.
    def auth_user(self, username, passcode, school_id):
        self.cursor.execute("""
        SELECT id FROM Users WHERE username = %s and passcode = %s and school_id = %s
        """,
        (username, passcode, school_id))

        record = self.cursor.fetchone()
        if record:
            return True
        else:
            return False


    #
    #   DATA FETCHING FUNCTIONS
    # TODO: fix all these functions!!!

    def fetch_all_questions(self):
        self.cursor.execute("""
        SELECT * FROM Question
        """)
        
        return self.cursor.fetchall()

    def fetch_question(self, question_id):
        self.cursor.execute("""
        SELECT * FROM Question
        WHERE Question.id = %s
        """,
        (question_id,))

        return self.cursor.fetchone()

    def fetch_answers(self, question_id):
        self.cursor.execute("""
        SELECT * FROM Answer
        WHERE question_id = %s
        """,
        (question_id,))
        return self.cursor.fetchall()

    def fetch_question_and_answers(self, question_id):
        question = self.fetch_question(question_id)
        answers = self.fetch_answers(question_id)

        return (question, answers)



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

    # TODO: Needs to fetch all the users questions they've answered. But multiple questions are repeated.. need to return each question_id only once.
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

    def add_questions(self, question_class, answer_class_list):
        question = question_class
        q_id = self.insert_question(question)
        question.question_id = q_id
        
        for record in answer_class_list:
            
            record.question_id = q_id
            self.insert_answer(record)


    def insert_answer(self, answer_class):
        self.cursor.execute("""
        INSERT INTO Answer (question_id, answer_id, correct, answer)
        SELECT %s,
            COUNT(*) + 1,
            %s,
            %s
        FROM Answer
        WHERE question_id = %s;
        """,
        (answer_class.question_id, answer_class.correct, answer_class.answer, answer_class.question_id))
        self.conn.commit()

    def insert_difficulty(self, difficulty_class):
        self.cursor.execute("""
        INSERT INTO Difficulty (id, name)
        VALUES (%s, %s)
        """,
        (difficulty_class.id, difficulty_class.name))
        self.conn.commit()

    def insert_question(self, question_class):
        self.cursor.execute("""
        INSERT INTO Question (question, difficulty_id, topic_id, subject_id)
        VALUES (%s, %s, %s, %s)
        RETURNING id; """,
        (question_class.question, question_class.difficulty_id, question_class.topic_id, question_class.subject_id))
        
        q_id = self.cursor.fetchone()[0]
        self.conn.commit()
        return q_id  # return ID so the code knows what the new ID is.
    
    def insert_question_answered(self, questionanswered_class):
        self.cursor.execute(f"""
        INSERT INTO QuestionAnswered (user_id, question_id, answer_id)
        VALUES (%s, %s, %s, %s)
        """,
        (questionanswered_class.user_id, questionanswered_class.question_id, questionanswered_class.answer_id))

        self.conn.commit()
    
    def insert_school(self, school_class):
        self.cursor.execute("""
        INSERT INTO School (name, contact)
        VALUES (%s, %s)
        RETURNING id;
        """,
        (school_class.name, school_class.contact))
        
        s_id = self.cursor.fetchone()[0]
        self.conn.commit()
        return s_id  # return ID so the code knows what the new ID is.

    def insert_subject(self, subject_class):
        self.cursor.execute("""
        INSERT INTO Subject (id, name)
        VALUES (%s, %s)
        """,
        (subject_class.id, subject_class.name))
        self.conn.commit()

    def insert_teacher(self, teacher_class):
        self.cursor.execute("""
        INSERT INTO Teacher (username, passcode, school_id)
        VALUES (%s, %s, %s)
        RETURNING id;
        """,
        (teacher_class.username, teacher_class.passcode, teacher_class.school_id))
        
        t_id = self.cursor.fetchone()[0]
        self.conn.commit()
        return t_id  # return ID so the code knows what the new ID is.

    def insert_topic(self, topic_class):
        self.cursor.execute("""
        INSERT INTO Topic (id, name, subject_id)
        VALUES (%s, %s, %s)
        """,
        (topic_class.id, topic_class.name, topic_class.subject_id))
        self.conn.commit()

    def insert_user(self, users_class):
        self.cursor.execute("""
        INSERT INTO Users (name, username, passcode, nickname, year_group_id, school_id)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id;
        """,
        (users_class.name, users_class.username, users_class.passcode, users_class.nickname, users_class.year_group_id, users_class.school_id))
        
        u_id = self.cursor.fetchone()[0]
        self.conn.commit()
        return u_id  # return ID so the code knows what the new ID is.

    def insert_year_group(self, yeargroup_class):
        self.cursor.execute("""
        INSERT INTO YearGroup (id, name)
        VALUES (%s, %s)
        """,
        (yeargroup_class.id, yeargroup_class.name))
        self.conn.commit()


    

    #
    #   SETUP FUNCTIONS
    # TODO: Fix these functions!!!!
    
    def setup_dummy_data(self):
        self.insert_difficulty(Difficulty(1, 'Very Easy'))
        self.insert_difficulty(Difficulty(2, 'Easy'))
        self.insert_difficulty(Difficulty(3, 'Medium'))
        self.insert_difficulty(Difficulty(4, 'Hard', ))
        self.insert_difficulty(Difficulty(5, 'Very Hard', ))

        self.insert_subject(Subject('MATHS', 'Maths'))

        self.insert_topic(Topic('PERCENTAGE', 'Percentages', 'MATHS'))
        self.insert_topic(Topic('ADDITION', 'Additions', 'MATHS'))
        self.insert_topic(Topic('SUBTRACTION', 'Subtractions', 'MATHS'))
        self.insert_topic(Topic('MULTIPLICATION', 'Multiplications', 'MATHS'))
        self.insert_topic(Topic('DIVISION', 'Divisions', 'MATHS'))



        self.insert_school(School('Cowes Enterprise College', 'reece_it@cowes.com'))
        self.insert_school(School('The International School for Spies'))

        self.insert_year_group(YearGroup(7, "Year 7"))
        self.insert_year_group(YearGroup(8, "Year 8"))
        self.insert_year_group(YearGroup(9, "Year 9"))
        self.insert_year_group(YearGroup(10, "Year 10"))
        self.insert_year_group(YearGroup(11, "Year 11"))
        self.insert_year_group(YearGroup(12, "Year 12"))
        self.insert_year_group(YearGroup(13, "Year 13"))


        
        self.insert_user(User('Reece', 'rnicholls13', '5678', 'The R', 13, 1))

        self.insert_teacher(Teacher("admin@cowes.com", 1234, 1))

        self.add_questions(Question("What is 10x10?", 1, "MULTIPLICATION", "MATHS"), 
                                    [Answer(True, '100'),
                                     Answer(False, '110')])
        self.insert_answer(Answer(True, '1010', 1))


        # self.add_question( Question("What is 10x10?", "100", "110", "1010", "120", "MATHS", "1") )
        # self.add_question( Question("What is 25% of 8?", '2', '4', '3', '1', 'MATHS', '3') )
        # self.add_question( Question("How many sides does a pentagon have?", '5', '4', '6', '7', 'MATHS', '1') )
        # self.add_question( Question("What is 25+7", '32', '33', '31', '34', 'MATHS', '3') )
        # self.add_question( Question("Whats the gradient of y=3x+4", '3', '3/4', '4/3', '4', 'MATHS', '5') )





# 
#   Database classes (used as data structures)
# 

class School:
    def __init__(self, name, contact=None, id=None):
        self.id = id
        self.name = name
        self.contact = contact


class Difficulty:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class Subject:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class YearGroup:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class Topic:
    def __init__(self, id, name, subject_id):
        self.id = id
        self.name = name
        self.subject_id = subject_id


class Teacher:
    def __init__(self, username, passcode, school_id, id=None):
        self.id = id
        self.username = username
        self.passcode = passcode
        self.school_id = school_id


class User:
    def __init__(self, name, username, passcode, nickname, year_group_id, school_id, id=None):
        self.id = id
        self.name = name
        self.username = username
        self.passcode = passcode
        self.nickname = nickname
        self.year_group_id = year_group_id
        self.school_id = school_id


class Question:
    def __init__(self, question, difficulty_id, topic_id, subject_id, id=None):
        self.id = id
        self.question = question
        self.difficulty_id = difficulty_id
        self.topic_id = topic_id
        self.subject_id = subject_id


class Answer:
    def __init__(self, correct, answer, question_id=None, answer_id=None):
        self.question_id = question_id
        self.answer_id = answer_id
        self.correct = correct
        self.answer = answer


class QuestionAnswered:
    def __init__(self, user_id, question_id, answer_id, time=None):
        self.user_id = user_id
        self.question_id = question_id
        self.answer_id = answer_id
        self.time = time


if __name__ == "__main__":
    d = DatabaseManager(psycopg2.connect("dbname='database1' user=postgres password='pass' host='localhost' port='5432'"))

    # d.insert_user(User('Sir', '0000', 'sir@cowes.com', '1'))

    # d.setup()
    # d.setup_dummy_data()
    
    print(d.auth_user('rnicholls13', '5678', 1))
    print(d.auth_user('rnicholls13', '2468', 1))
    print(d.fetch_question(1))
    print(d.fetch_question_and_answers(1))