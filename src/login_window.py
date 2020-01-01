import tkinter as tk

class Login:
    def __init__(self):
        self.window = tk.Tk()
        self.email = None
        self.passcode = None

    def login_pressed(self):
        self.email = self.email_entry.get()
        self.passcode = self.passcode_entry.get()
        self.window.destroy()

    def draw_window(self):
        self.welcome_label = tk.Label(self.window, text="Welcome!")
        self.welcome_label.grid(row=0, column=0, rowspan=1, columnspan=2)

        # email
        self.email_label = tk.Label(self.window, text="Email")
        self.email_label.grid(row=1, column=0)

        self.email_entry = tk.Entry(self.window, bd=1)
        self.email_entry.grid(row=1, column=1)

        # passcode
        self.passcode_label = tk.Label(self.window, text="Passcode")
        self.passcode_label.grid(row=2, column=0)

        self.passcode_entry = tk.Entry(self.window, bd=1)
        self.passcode_entry.grid(row=2, column=1)

        # login
        self.login_button = tk.Button(self.window, text="Login", command=self.login_pressed)
        self.login_button.grid(row=3, column=0, columnspan=2, ipadx=5, pady=5)

        self.window.mainloop()
    
if __name__ == "__main__":
    log = Login()
    log.draw_window()
    print(log.email)
    print(log.passcode)