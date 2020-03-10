import psycopg2
import psycopg2.extras
import time
from .database_classes import School, Difficulty, Subject, YearGroup, Topic, Teacher, User, Question, Answer, QuestionAnswered


class DatabaseManager:
    def __init__(self, conn):
        self.conn = conn
        # the cursor factory returns each row in the database as a dictionary item.
        self.cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


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
    #

    def fetch_all_questions(self):
        self.cursor.execute("""
        SELECT * FROM Question
        """)

        return self.cursor.fetchall()

    # Randomises the questions.
    def fetch_questions_by_topic(self, topic_class):
        self.cursor.execute("""
        SELECT * FROM Question
        WHERE Question.topic_id = %s AND Question.subject_id = %s
        ORDER BY RANDOM()
        """,
        (topic_class.id, topic_class.subject_id))
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

    # This returns a tuple. First index is a question, the next index is a list of answers.
    def fetch_question_and_answers(self, question_id):
        question = self.fetch_question(question_id)
        answers = self.fetch_answers(question_id)

        return (question, answers)


    def fetch_user(self, username, school_id):
        self.cursor.execute("""
        SELECT * FROM Users
        WHERE username = %s AND school_id = %s
        """,
        (username, school_id))
        return self.cursor.fetchone()
    
    def fetch_user_using_id(self, user_id):
        self.cursor.execute("""
        SELECT * FROM Users
        WHERE id = %s
        """,
        (user_id,))
        return self.cursor.fetchone()

    def fetch_all_subjects(self):
        self.cursor.execute("""
        SELECT * FROM Subject
        """)
        return self.cursor.fetchall()

    def fetch_all_schools(self):
        self.cursor.execute("""
        SELECT * FROM School
        """)
        return self.cursor.fetchall()
    
    def fetch_subject(self, subject_id):
        self.cursor.execute("""
        SELECT * FROM Subject
        WHERE id = %s
        """,
        (subject_id,))
        return self.cursor.fetchone()
    
    def fetch_topic_by_subject(self, subject_id):
        self.cursor.execute("""
        SELECT * FROM Topic
        WHERE subject_id = %s
        """,
        (subject_id,))
        return self.cursor.fetchall()
    
    def fetch_school(self, school_id):
        self.cursor.execute("""
        SELECT * FROM School
        WHERE id = %s
        """,
        (school_id,))
        return self.cursor.fetchone()

    def fetch_schools_users(self, school_id):
        self.cursor.execute("""
        SELECT * FROM Users
        WHERE school_id = %s
        """,
        (school_id,))
        return self.cursor.fetchall()

    def fetch_question_answered_by_user(self, user_id, question_id):
        self.cursor.execute("""
        SELECT QuestionAnswered.user_id, QuestionAnswered.question_id, QuestionAnswered.answer_id, Answer.correct, Answer.answer, QuestionAnswered.time FROM QuestionAnswered
		JOIN Answer ON QuestionAnswered.question_id = Answer.question_id AND QuestionAnswered.answer_id = Answer.answer_id
        WHERE QuestionAnswered.user_id = %s AND QuestionAnswered.question_id = %s
        ORDER BY time DESC
        """,
        (user_id, question_id))
        return self.cursor.fetchall()

    def fetch_all_questions_answered_by_user(self, user_id):
        self.cursor.execute("""
        SELECT * FROM QuestionAnswered
        WHERE user_id = %s
        ORDER BY question_id, time
        """,
        (user_id,))
        return self.cursor.fetchall()

    def fetch_all_question_names_answered_by_user(self, user_id):
        self.cursor.execute("""
        SELECT DISTINCT ON (QuestionAnswered.user_id, QuestionAnswered.question_id) QuestionAnswered.user_id, QuestionAnswered.question_id, Question.question FROM QuestionAnswered
        JOIN Question ON QuestionAnswered.question_id = Question.id
		WHERE QuestionAnswered.user_id = %s
        ORDER BY QuestionAnswered.question_id
        """,
        (user_id,))
        return self.cursor.fetchall()

    # LEADERBOARD FETCHING FUNCTIONS

    # TODO: Fix this! Done!
    def fetch_user_total_score(self, user_id):
        self.cursor.execute("""
        WITH summary AS (SELECT DISTINCT ON (QuestionAnswered.user_id, QuestionAnswered.question_id) QuestionAnswered.user_id, Users.name AS user_name, Users.nickname AS user_nickname, School.name AS school_name, QuestionAnswered.question_id, QuestionAnswered.answer_id, Answer.correct, Question.difficulty_id, QuestionAnswered.time FROM QuestionAnswered
        JOIN Question ON QuestionAnswered.question_id = Question.id
        JOIN Answer ON QuestionAnswered.answer_id = Answer.answer_id AND QuestionAnswered.question_id = Answer.question_id
		JOIN Users ON QuestionAnswered.user_id = Users.id
		JOIN School ON Users.school_id = School.id	 
		GROUP BY QuestionAnswered.user_id, Users.name, Users.nickname, School.name, QuestionAnswered.question_id, QuestionAnswered.answer_id, Answer.correct, Question.difficulty_id, QuestionAnswered.time
		ORDER BY QuestionAnswered.user_id, QuestionAnswered.question_id, QuestionAnswered.time DESC
		)
		
		SELECT user_id, user_name, user_nickname, school_name, sum(difficulty_id) AS score FROM summary
		WHERE correct = true AND user_id = %s
		GROUP BY user_id, user_name, user_nickname, school_name
        ORDER BY score DESC
        """,
        (user_id,))
        return self.cursor.fetchone()


    def fetch_leaderboard_school_subject(self, school_id, subject_id):
        self.cursor.execute("""
        WITH summary AS (SELECT DISTINCT ON (QuestionAnswered.user_id, QuestionAnswered.question_id) QuestionAnswered.user_id,
            Users.name AS user_name, Users.nickname AS user_nickname, QuestionAnswered.question_id, QuestionAnswered.answer_id,
            Answer.correct, Question.difficulty_id, QuestionAnswered.time FROM QuestionAnswered
        JOIN Question ON QuestionAnswered.question_id = Question.id
        JOIN Answer ON QuestionAnswered.answer_id = Answer.answer_id AND QuestionAnswered.question_id = Answer.question_id
		JOIN Users ON QuestionAnswered.user_id = Users.id
		WHERE Users.school_id = %s AND Question.subject_id = %s
		GROUP BY QuestionAnswered.user_id, Users.name, Users.nickname, QuestionAnswered.question_id, QuestionAnswered.answer_id,
            Answer.correct, Question.difficulty_id, QuestionAnswered.time
		ORDER BY QuestionAnswered.user_id, QuestionAnswered.question_id, QuestionAnswered.time DESC
		)
		
		SELECT user_id, user_name, user_nickname, sum(difficulty_id) AS score FROM summary
		WHERE correct = true
		GROUP BY user_id, user_name, user_nickname
        ORDER BY score DESC
        """,
        (school_id, subject_id))

        return self.cursor.fetchall()

    # TODO: Fix this! Fixed, just need to test it. Tests pass, function is now completely fixed!
    def fetch_leaderboard_school(self, school_id):
        self.cursor.execute("""
        WITH summary AS (SELECT DISTINCT ON (QuestionAnswered.user_id, QuestionAnswered.question_id) QuestionAnswered.user_id, Users.name AS user_name, Users.nickname AS user_nickname, QuestionAnswered.question_id, QuestionAnswered.answer_id, Answer.correct, Question.difficulty_id, QuestionAnswered.time FROM QuestionAnswered
        JOIN Question ON QuestionAnswered.question_id = Question.id
        JOIN Answer ON QuestionAnswered.answer_id = Answer.answer_id AND QuestionAnswered.question_id = Answer.question_id
		JOIN Users ON QuestionAnswered.user_id = Users.id
		WHERE Users.school_id = %s
		GROUP BY QuestionAnswered.user_id, Users.name, Users.nickname, QuestionAnswered.question_id, QuestionAnswered.answer_id, Answer.correct, Question.difficulty_id, QuestionAnswered.time
		ORDER BY QuestionAnswered.user_id, QuestionAnswered.question_id, QuestionAnswered.time DESC
		)
		
		SELECT user_id, user_name, user_nickname, sum(difficulty_id) AS score FROM summary
		WHERE correct = true
		GROUP BY user_id, user_name, user_nickname
        ORDER BY score DESC
        """,
        (school_id,))

        return self.cursor.fetchall()


    # Never touch this. it just works. Returns user_id, score, user_name, user_nickname, school_name.
    def fetch_leaderboard_global(self):
        # WORKING AS EXPECTED
        self.cursor.execute("""
        WITH summary AS (SELECT DISTINCT ON (QuestionAnswered.user_id, QuestionAnswered.question_id) QuestionAnswered.user_id, Users.name AS user_name, Users.nickname AS user_nickname, School.name AS school_name, QuestionAnswered.question_id, QuestionAnswered.answer_id, Answer.correct, Question.difficulty_id, QuestionAnswered.time FROM QuestionAnswered
        JOIN Question ON QuestionAnswered.question_id = Question.id
        JOIN Answer ON QuestionAnswered.answer_id = Answer.answer_id AND QuestionAnswered.question_id = Answer.question_id
		JOIN Users ON QuestionAnswered.user_id = Users.id
		JOIN School ON Users.school_id = School.id
		GROUP BY QuestionAnswered.user_id, Users.name, School.name, Users.nickname, QuestionAnswered.question_id, QuestionAnswered.answer_id, Answer.correct, Question.difficulty_id, QuestionAnswered.time
		ORDER BY QuestionAnswered.user_id, QuestionAnswered.question_id, QuestionAnswered.time DESC
		)
		
		SELECT user_id, sum(difficulty_id) AS score, user_name, user_nickname, school_name FROM summary
		WHERE correct = true
		GROUP BY user_id, user_name, user_nickname, school_name
        ORDER BY score DESC
        """)

        return self.cursor.fetchall()



    # 
    #   CORE INSERTING FUNCTIONS
    # 

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
        if questionanswered_class.time:
            self.cursor.execute("""
            INSERT INTO QuestionAnswered (user_id, question_id, answer_id, time)
            VALUES (%s, %s, %s, %s)
            """,
            (questionanswered_class.user_id, questionanswered_class.question_id, questionanswered_class.answer_id, questionanswered_class.time))
        else:
            self.cursor.execute("""
            INSERT INTO QuestionAnswered (user_id, question_id, answer_id)
            VALUES (%s, %s, %s)
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
    #   INSERTING FUNCTIONS
    # 

    # Provide question class, and a list containing each answer class.
    def add_question_with_answers(self, question_class, answer_class_list):
        question = question_class
        q_id = self.insert_question(question)
        # question.question_id = q_id # not needed any more.
        
        for record in answer_class_list:
            # populates the answers with the Question ID stored in the database.
            record.question_id = q_id
            self.insert_answer(record)



    

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
        self.insert_subject(Subject('COMP_SCI', 'Computer Science'))


        self.insert_topic(Topic('PERCENTAGE', 'Percentages', 'MATHS'))
        self.insert_topic(Topic('ADDITION', 'Additions', 'MATHS'))
        self.insert_topic(Topic('SUBTRACTION', 'Subtractions', 'MATHS'))
        self.insert_topic(Topic('MULTIPLICATION', 'Multiplications', 'MATHS'))
        self.insert_topic(Topic('DIVISION', 'Divisions', 'MATHS'))
        self.insert_topic(Topic('SHAPE', 'Shapes', 'MATHS'))

        self.insert_topic(Topic('PYTHON', 'Python', 'COMP_SCI'))



        self.insert_school(School('The International School for Spies'))
        self.insert_school(School('Cowes Enterprise College', 'reece_it@cowes.com'))

        self.insert_year_group(YearGroup(7, "Year 7"))
        self.insert_year_group(YearGroup(8, "Year 8"))
        self.insert_year_group(YearGroup(9, "Year 9"))
        self.insert_year_group(YearGroup(10, "Year 10"))
        self.insert_year_group(YearGroup(11, "Year 11"))
        self.insert_year_group(YearGroup(12, "Year 12"))
        self.insert_year_group(YearGroup(13, "Year 13"))


        
        self.insert_user(User('John', 'johnsmith', '0000', 'Dr Who', 13, 1))
        self.insert_user(User('Bob', 'bobj', '0000', 'BJ', 11, 1))
        self.insert_user(User('Reece', 'rnicholls13', '5678', 'The R', 13, 2))



        self.insert_teacher(Teacher("admin@cowes.com", 1234, 1))

        self.add_question_with_answers(Question("What is 10x10?", 1, "MULTIPLICATION", "MATHS"), 
                                       [Answer(True, '100'),
                                        Answer(False, '110'),
                                        Answer(False, '1010')])
        self.insert_answer(Answer(False, '120', 1))

        self.add_question_with_answers(Question("What is 25% of 8?", 4, 'PERCENTAGE', 'MATHS'),
                                       [Answer(True, '2'),
                                        Answer(False, '1'),
                                        Answer(False, '3'),
                                        Answer(False, '4')])

        self.add_question_with_answers(Question("How many sides does a pentagon have?", 1, 'SHAPE', 'MATHS'),
                                       [Answer(True, '5'),
                                        Answer(False, '4'),
                                        Answer(False, '6'),
                                        Answer(False, '7')                                        
                                        ])

        self.add_question_with_answers(Question("Does this statement produce an error: print(Hello)", 1, 'PYTHON', 'COMP_SCI'),
                                       [Answer(True, 'No'),
                                        Answer(False, 'Yes')])

        self.add_question_with_answers(Question("What is 50% of 30?", 2, 'PERCENTAGE', 'MATHS'),
                                       [Answer(True, '15'),
                                        Answer(False, '25'),
                                        Answer(False, '60'),
                                        Answer(False, '10')])

        self.add_question_with_answers(Question("What is 75% of 60?", 5, 'PERCENTAGE', 'MATHS'),
                                       [Answer(True, '45'),
                                        Answer(False, '35'),
                                        Answer(False, '50'),
                                        Answer(False, '30')])

        self.insert_question_answered(QuestionAnswered(1, 1, 1))
        self.insert_question_answered(QuestionAnswered(1, 1, 2))
        self.insert_question_answered(QuestionAnswered(1, 1, 1))
        self.insert_question_answered(QuestionAnswered(1, 1, 3))
        self.insert_question_answered(QuestionAnswered(1, 1, 1))

        self.insert_question_answered(QuestionAnswered(1, 2, 2))
        self.insert_question_answered(QuestionAnswered(1, 2, 2))
        self.insert_question_answered(QuestionAnswered(1, 2, 1))
        self.insert_question_answered(QuestionAnswered(1, 2, 1))

        self.insert_question_answered(QuestionAnswered(1, 3, 2))
        self.insert_question_answered(QuestionAnswered(1, 3, 1))

        self.insert_question_answered(QuestionAnswered(2, 1, 1))
        self.insert_question_answered(QuestionAnswered(2, 2, 1))
        self.insert_question_answered(QuestionAnswered(2, 3, 2))
        self.insert_question_answered(QuestionAnswered(1, 4, 1))

        print("Successfully reset and recreated the database!")

        # self.add_question( Question("What is 10x10?", "100", "110", "1010", "120", "MATHS", "1") )
        # self.add_question( Question("What is 25% of 8?", '2', '4', '3', '1', 'MATHS', '3') )
        # self.add_question( Question("How many sides does a pentagon have?", '5', '4', '6', '7', 'MATHS', '1') )
        # self.add_question( Question("What is 25+7", '32', '33', '31', '34', 'MATHS', '3') )
        # self.add_question( Question("Whats the gradient of y=3x+4", '3', '3/4', '4/3', '4', 'MATHS', '5') )




if __name__ == "__main__":
    print("Run using the run_*.py file in the root directory.")