from database.database_manager import DatabaseManager
from database.database_classes import School, Difficulty, Subject, YearGroup, Topic, Teacher, User, Question, Answer, QuestionAnswered

import psycopg2
import unittest
import datetime


class TestAuthUser(unittest.TestCase):

    def test_auth_user_normal(self):
        self.assertEqual(d.auth_user('rnicholls13', '5678', 2), True, "Normal auth user correct failed")
    
    def test_auth_user_normal_incorrect(self):
        self.assertEqual(d.auth_user('rnicholls13', '0000', 2), False, "Normal auth user incorrect failed")


class TestFetchQuestion(unittest.TestCase):

    def test_fetch_question_normal(self):
        q = d.fetch_question(1)
        self.assertEqual(q, [1, 'What is 10x10?', 1, 'MULTIPLICATION', 'MATHS'], "Normal fetch question id=1 failed")
        self.assertEqual(q['id'], 1, "ID test failed")
        self.assertEqual(q['topic_id'], 'MULTIPLICATION', "Topic ID test failed")

    def test_fetch_question_normal_incorrect(self):
        self.assertNotEqual(d.fetch_question(1), [2, 'WrongQuestion', 1, 'FAKETOPIC', 'FAKESUBJECT'])


class TestFetchQuestionAndAnswers(unittest.TestCase):

    def test_fetch_question_and_answer_normal(self):
        result = d.fetch_question_and_answers(1)
        self.assertEqual(result[0]['id'], 1, "ID doesn't match")
        self.assertEqual(result[0]['question'], "What is 10x10?", "Question text doesn't match.")
        self.assertEqual(result[0]['topic_id'], 'MULTIPLICATION', "Topic ID doesn't match")
        self.assertEqual(result[0]['subject_id'], 'MATHS', "Topic ID doesn't match")

        self.assertEqual(result[1][0]['answer'], '100', "Correct answer doesn't match")
        self.assertEqual(result[1][0]['correct'], True, "Correct 'correct' doesn't match")
        for answer in result[1]:
            self.assertEqual(answer['question_id'], 1, "Answer question_id does not match true question id.")

        self.assertNotEqual(result[1][1]['answer'], '100', "Incorrect answer doesn't match")


class TestFetchLeaderboardGlobal(unittest.TestCase):
   
    def test_fetch_leaderboard_global_normal(self):
        result = d.fetch_leaderboard_global()
        
        self.assertEqual(result[0]['user_id'], 1, "User_ID isn't what it should be")
        self.assertEqual(result[0]['score'], 7, "Score isn't what it should be")
        self.assertEqual(result[0]['user_name'], "John", "Name isn't what it should be")
        self.assertEqual(result[0]['user_nickname'], "Dr Who", "Nick isn't what it should be")
        self.assertEqual(result[0]['school_name'], "The International School for Spies", "School name isn't what it should be")

        self.assertEqual(result[1]['user_id'], 2, "School User_ID doesn't match")
        self.assertEqual(result[1]['score'], 5, "School score doesn't match")
        self.assertEqual(result[1]['user_name'], "Bob", "Name isn't what it should be")
        self.assertEqual(result[1]['user_nickname'], "BJ", "Nick isn't what it should be")




class TestFetchLeaderboardSchool(unittest.TestCase):

    def test_fetch_leaderboard_school_normal(self):
        # Test school id 1 to make sure dummy data matches.
        result = d.fetch_leaderboard_school(1)

        self.assertEqual(result[0]['user_id'], 1, "School User_ID doesn't match")
        self.assertEqual(result[0]['score'], 7, "School score doesn't match")
        self.assertEqual(result[0]['user_name'], "John", "Name isn't what it should be")
        self.assertEqual(result[0]['user_nickname'], "Dr Who", "Nick isn't what it should be")

        self.assertEqual(result[1]['user_id'], 2, "School User_ID doesn't match")
        self.assertEqual(result[1]['score'], 5, "School score doesn't match")
        self.assertEqual(result[1]['user_name'], "Bob", "Name isn't what it should be")
        self.assertEqual(result[1]['user_nickname'], "BJ", "Nick isn't what it should be")



class TestFetchLeadboardSchoolSubject(unittest.TestCase):

    def test_fetch_leaderboard_school_subject_normal(self):
        result = d.fetch_leaderboard_school_subject(1, 'MATHS')

        self.assertEqual(result[0]['user_id'], 1, "1st place User_ID not matching")
        self.assertEqual(result[0]['score'], 6, "1st place score not matching")
        self.assertEqual(result[0]['user_name'], "John", "Name isn't what it should be")
        self.assertEqual(result[0]['user_nickname'], "Dr Who", "Nick isn't what it should be")

        self.assertEqual(result[1]['user_id'], 2, "2nd place User_ID not matching")
        self.assertEqual(result[1]['score'], 5, "2nd place score not matching")
        self.assertEqual(result[1]['user_name'], "Bob", "Name isn't what it should be")
        self.assertEqual(result[1]['user_nickname'], "BJ", "Nick isn't what it should be")


class TestFetchUserTotalScore(unittest.TestCase):

    def test_fetch_user_total_score_normal(self):
        result = d.fetch_user_total_score(1)
        self.assertEqual(result['user_id'], 1, 'User_ID not matching')
        self.assertEqual(result['score'], 7, 'Score not matching')

        result = d.fetch_user_total_score(2)
        self.assertEqual(result['user_id'], 2, 'User_ID not matching')
        self.assertEqual(result['score'], 5, 'Score not matching')


class TestFetchQuestionsByTopic(unittest.TestCase):

    def test_fetch_questions_by_topic_normal(self):
        result = d.fetch_questions_by_topic(Topic(id='PERCENTAGE', name=None, subject_id='MATHS'))
        print(result)

def run(db_config_string):
    global d
    # d = DatabaseManager(psycopg2.connect(db_config_string))
    d = DatabaseManager(psycopg2.connect(db_config_string))

    unittest.main()

if __name__ == "__main__":
    print("Running tests from root directory")
    