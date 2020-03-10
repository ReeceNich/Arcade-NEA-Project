import tkinter as tk


class Login:
    def __init__(self, database_manager):
        self.window = tk.Tk()
        self.window.title("Login - Falling Man")
        self.db = database_manager

        # responsible for getting the list of schools
        self.raw_schools = self.db.fetch_all_schools()
        self.school_name_list = []

        for row in self.raw_schools:
            self.school_name_list.append(row['name'])


        # responsible for getting the list of subjects
        self.raw_subjects = self.db.fetch_all_subjects()
        self.subject_name_list = []

        for row in self.raw_subjects:
            self.subject_name_list.append(row['name'])


        self.topic_name_list = [""]
        self.username = None
        self.passcode = None
        self.school_id = None
        self.subject_id = None
        self.topic_id = None

    def login_pressed(self):
        self.username = self.username_entry.get()
        self.passcode = self.passcode_entry.get()
        self.school_name = self.school_list_var.get()
        self.subject_name = self.subject_list_var.get()
        self.topic_name = self.topic_list_var.get()

        # given the schools name, find the ID of the school.
        for row in self.raw_schools:
            if self.school_name == row['name']:
                self.school_id = row['id']
                break

        # given the topic name and subject id, find the ID of the topic.
        for row in self.raw_topics:
            if self.topic_name == row['name'] and self.subject_id == row['subject_id']:
                self.topic_id = row['id']
                break


        print(f"Username: {self.username}, School_id: {self.school_id}, subject_id: {self.subject_id}, topic_id: {self.topic_id}")

        self.window.destroy()


    def subject_selected(self, *args):
        print(args[0])
        # given the subjects name, find the ID of the subject.
        for row in self.raw_subjects:
            if args[0] == row['name']:
                self.subject_id = row['id']
                break
        
        print(f"subjectid: {self.subject_id}.")
        self.get_topics()

    def get_topics(self):
        # responsible for getting the list of topics
        self.raw_topics = self.db.fetch_topic_by_subject(self.subject_id)
        self.topic_name_list = []

        for row in self.raw_topics:
            self.topic_name_list.append(row['name'])

        print(f"rawtopics: {self.raw_topics}.")
        print(f"topic name list: {self.topic_name_list}.")

        self.topic_list_label = tk.Label(self.window, text="Topic")
        self.topic_list_label.grid(row=5, column=0)

        self.topic_list_var = tk.StringVar(self.window)
        self.topic_list_var.set("-- Select a topic --")
        topic_dropdown = tk.OptionMenu(self.window, self.topic_list_var, "-- Select a topic --", *self.topic_name_list)
        topic_dropdown.grid(row=5, column=1)


    def draw_window(self):
        self.welcome_label = tk.Label(self.window, text="Welcome to Falling Man!")
        self.welcome_label.grid(row=0, column=0, rowspan=1, columnspan=2)

        # username
        self.username_label = tk.Label(self.window, text="Username")
        self.username_label.grid(row=1, column=0)

        self.username_entry = tk.Entry(self.window, bd=1)
        self.username_entry.grid(row=1, column=1)

        # passcode
        self.passcode_label = tk.Label(self.window, text="Passcode")
        self.passcode_label.grid(row=2, column=0)

        self.passcode_entry = tk.Entry(self.window, bd=1)
        self.passcode_entry.grid(row=2, column=1)

        # list of schools
        self.school_list_label = tk.Label(self.window, text="School")
        self.school_list_label.grid(row=3, column=0)

        self.school_list_var = tk.StringVar(self.window)
        self.school_list_var.set("-- Select a school --")
        school_dropdown = tk.OptionMenu(self.window, self.school_list_var, "-- Select a school --", *self.school_name_list)
        school_dropdown.grid(row=3, column=1)

        # list of subjects
        self.subject_list_label = tk.Label(self.window, text="Subject")
        self.subject_list_label.grid(row=4, column=0)

        self.subject_list_var = tk.StringVar(self.window)
        self.subject_list_var.set("-- Select a subject --")
        subject_dropdown = tk.OptionMenu(self.window, self.subject_list_var, "-- Select a subject --", *self.subject_name_list, command=self.subject_selected)
        subject_dropdown.grid(row=4, column=1)


        # login
        self.login_button = tk.Button(self.window, text="Login", command=self.login_pressed)
        self.login_button.grid(row=6, column=0, columnspan=2, ipadx=5, pady=5)

        self.window.mainloop()
    
if __name__ == "__main__":
    print("Run through the run_*.py script in the root directory.")