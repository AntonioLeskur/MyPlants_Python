import tkinter
import sql_file
from tkinter import messagebox
import random
import pyperclip
import values_file

# Starting window, that is also a log in window


class LogInWindow(tkinter.Tk):
    sql_in = sql_file.UsersSql()
    sql_in.create_user_table()
    sql_in.create_current_user_db()
    sql_in.import_starting_users()

    def __init__(self):
        super().__init__()
        window = self
        ICON = tkinter.PhotoImage(file="images_icons/leaf.png")

        window.title("MyPlants")
        window.config(pady=20, padx=20, bg="white")
        window.iconphoto(False, ICON)

        canvas = tkinter.Canvas(width=200, height=200, bg="white", highlightthickness=0)

        image = tkinter.PhotoImage(file="images_icons/tree.png")
        canvas.create_image(114, 100, image=image)
        canvas.grid(column=1, row=0)

        username_text = tkinter.Label(text="Email/Username:", bg="white")
        username_text.grid(sticky="E", column=0, row=1)

        self.username_entry = tkinter.Entry(width=33)
        self.username_entry.insert(0, "Admin")
        self.username_entry.grid(sticky="W", column=1, row=1, columnspan=2)

        password_text = tkinter.Label(text="Password:", bg="white")
        password_text.grid(sticky="E", column=0, row=2)

        self.password_entry = tkinter.Entry(width=33)
        self.password_entry.insert(0, "admin")
        self.password_entry.grid(sticky="W", column=1, row=2)

        generate_button = tkinter.Button(text="Generate Password", width=15, bg="#FFFFFF", bd=1, command=self.pass_gen)
        generate_button.grid(sticky="W", column=2, row=2)

        add_button = tkinter.Button(text="Add", width=27, bg="#FFFFFF", bd=1, command=self.save)
        add_button.grid(sticky="W", column=1, row=3, pady=3)

        login_button = tkinter.Button(text="Log in", width=15, bg="#FFFFFF", bd=1, command=self.log_in)
        login_button.grid(sticky="W", column=2, row=3, pady=3)
        window.mainloop()

    def log_in(self):

        # If current_user table is empty, it means it is the first log in ever, therefore the program will import
        # starting plant database table
        # Otherwise, if you want to import starting plant database table, you will have to do it manually
        # or delete both databases (plant_datab.db, users.db) and restart the program

        import main_window_file
        user = self.sql_in.cur.execute("SELECT * FROM current_user").fetchall()
        if len(user) < 1:
            sql_file.PlantSql().create_plant_table()
            sql_file.PlantSql().import_starting_plants()
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.sql_in.cur.execute("SELECT * FROM users WHERE username=? and password=?", [username, password])

        if self.sql_in.cur.fetchone() == None:
            tkinter.messagebox.showinfo(title="Oops", message="Please check your username/password.")
        else:

            # Making current_user table that will be used later to check if the logged user is Admin
            # because of their possibilities to make certain changes

            self.sql_in.cur.execute("DROP TABLE current_user")
            self.sql_in.create_current_user_db()
            self.sql_in.cur.execute("SELECT * FROM current_user")
            CURRENT_USER = self.sql_in.cur.execute("SELECT * FROM users WHERE username=? and password=?",
                                       [username, password]).fetchone()
            self.sql_in.cur.execute(f"""
            INSERT OR REPLACE INTO current_user (id, username, password) VALUES
            ('{CURRENT_USER[0]}', '{CURRENT_USER[1]}', '{CURRENT_USER[2]}')
            """)
            self.sql_in.conn.commit()
            self.destroy()
            self.main_window = main_window_file.MainWindow()

    def save(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if len(username) == 0 or len(password) == 0 or len(username) == 0:
            tkinter.messagebox.showinfo(title="Oops", message="Please don't leve any fields empty.")

        else:
            is_ok = tkinter.messagebox.askokcancel(title=username,
                                                   message=f"These are the data entered: \nUsername: {username} "
                                                           f"\nPassword: {password}\nIs it ok to save?")
            if is_ok:
                self.sql_in.add_user(self.sql_in.conn, username, password)
                self.username_entry.delete(0, tkinter.END)
                self.password_entry.delete(0, tkinter.END)

# Password generator

    def pass_gen(self):
        self.password_entry.delete(0, tkinter.END)
        password_letters = [random.choice(values_file.letters) for x in range(0, 6)]
        password_numbers = [random.choice(values_file.numbers) for x in range(0, 2)]
        password_symbols = [random.choice(values_file.symbols) for x in range(0, 2)]
        password_gen = password_symbols + password_numbers + password_letters
        random.shuffle(password_gen)
        password_new = "".join(password_gen)
        pyperclip.copy(password_new)
        self.password_entry.insert(0, password_new)
