# 
#   Database classes (used as data structures)
# 
import datetime


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