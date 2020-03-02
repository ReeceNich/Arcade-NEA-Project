from database_manager import *
import unittest

d = DatabaseManager(psycopg2.connect("dbname='database1' user=postgres password='pass' host='localhost' port='5432'"))


class TestAuthUser(unittest.TestCase):

    def test_auth_user_normal(self):
        self.assertEqual(d.auth_user('rnicholls13', '5678', 1), True, "Normal auth user correct failed")
    
    def test_auth_user_normal_incorrect(self):
        self.assertEqual(d.auth_user('rnicholls13', '0000', 1), False, "Normal auth user incorrect failed")


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
        self.assertEqual(result[0]['topic_id'], 'MULTIPLICATION', "Topic ID doesn't match")
        self.assertEqual(result[0]['subject_id'], 'MATHS', "Topic ID doesn't match")

        self.assertEqual(result[1][0]['answer'], '100', "Correct answer doesn't match")
        self.assertEqual(result[1][0]['correct'], True, "Correct 'correct' doesn't match")

        self.assertNotEqual(result[1][1]['answer'], '100', "Incorrect answer doesn't match")




if __name__ == "__main__":
    # d = DatabaseManager(psycopg2.connect("dbname='database1' user=postgres password='pass' host='localhost' port='5432'"))

    unittest.main()