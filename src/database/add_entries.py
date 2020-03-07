from database.database_manager import *
from database.database_classes import *
import psycopg2
import random


### MAIN PROGRAM STARTS HERE ###

def get_choice(options):
    while True:
        try:
            choice = int(input("Enter a choice > "))
            if choice in options:
                return choice
            else:
                print("Invalid choice, try again...")
        except:
            print("Invalid choice, try again...")


def main(db_config_string):
    db = DatabaseManager(psycopg2.connect(db_config_string))

    print("Welcome to the database management system")
    print("")
    print("Here are your options:")

    options = {
        1: "Add a school",
        2: "Add a year group",
        3: "Add a difficulty",
        4: "Add a subject",
        
        5: "Add a topic",
        6: "Add a user",
        7: "Add a teacher",
        8: "Add a question",
        9: "Add an answer",
        10: "Add a QuestionAnswered",
        0: "Exit"
    }
    for key, value in options.items():
        print(f"{key}. {value}")
    print("")

    choice = get_choice(options)
    
    print("")
    print(f"*** SELECTED: {options[choice]} ***")
    if choice == 0:
        exit()

    elif choice == 1:
        name = input("Enter the school name > ")
        contact = input("Enter the contact info (leave blank if none) > ")

        school = School(name, contact)
        s_id = db.insert_school(school)
        print("")
        print(f"New school ID is: {s_id}")

    elif choice == 2:
        name = input("Enter the year group name > ")
        id = input("Enter the ID (number of the year group) > ")
        yeargroup = YearGroup(id, name)
        db.insert_year_group(yeargroup)

    elif choice == 3:
        name = input("Enter difficulty name > ")
        id = int(input("Enter difficulty ID > "))
        diff = Difficulty(id, name)
        db.insert_difficulty(diff)

    elif choice == 4:
        name = input("Enter subject name > ")
        id = input("Enter subject ID > ")
        sub = Subject(id, name)
        db.insert_subject(sub)


    # ALL THESE FUNCTIONS REQUIRE TABLES FROM ABOVE.

    elif choice == 5:
        name = input("Enter topic name > ")
        id = input("Enter topic ID > ")
        subject_id = input("Enter subject ID which should topic belong to > ")

        topic = Topic(id, name, subject_id)
        db.insert_topic(topic)

    elif choice == 6:
        name = input("Enter the users name > ")
        username = input("Enter the username (unique per school) > ")
        nickname = input("Enter a nickname (blank for none) > ")
        passcode = input("Enter a passcode (blank for random) > ")
        year_group_id = input("Enter year group ID > ")
        school_id = input("Enter their school ID > ")

        if passcode == "":
            passcode = random.randrange(1000, 9999)

        user = User(name, username, passcode, nickname, year_group_id, school_id)
        u_id = db.insert_user(user)
        print("")
        print(f"User's new ID is: {u_id}")

    elif choice == 7:
        username = input("Enter the username (unique per school) > ")
        passcode = input("Enter a passcode (blank for random) > ")
        school_id = input("Enter their school ID > ")
        
        if passcode == "":
            passcode = random.randrange(1000, 9999)

        teacher = Teacher(username, passcode, school_id)
        db.insert_teacher(teacher)
        print("")
        print(f"User's new ID is: {u_id}")

    elif choice == 8:
        q = input("Enter question > ")
        s_id = input("Enter subject ID for this question > ")
        t_id = input("Enter topic ID for this question > ")
        d_id = int(input("Enter difficulty ID for this question > "))
        
        question = Question(q, d_id, t_id, s_id)
        q_id = db.insert_question(question)
        print("")
        print(f"Question's new ID is: {q_id}")

    elif choice == 9:
        a = input("Enter the answer > ")
        correct = input("Is the answer a correct answer or not? (y/n) > ")
        q_id = input("Enter the question ID the answer should belong to > ")
        answer = Answer(correct, a, q_id)
        db.insert_answer(answer)

    elif choice == 10:
        u_id = input("Enter the user's ID > ")
        q_id = input("Enter the question ID > ")
        a_id = input("Enter the answer ID > ")

        q_a = QuestionAnswered(u_id, q_id, a_id)
        db.insert_question_answered(q_a)

    else:
        pass
    
    print(f"*** END SELECTED: {options[choice]}")


if __name__ == "__main__":
    print("Please run through the run_*.py script in the root directory.")