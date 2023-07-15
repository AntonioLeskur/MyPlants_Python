import tkinter
import sql_file

# Window that shows user info


class AccountInfo(tkinter.Toplevel):

    def __init__(self):
        super().__init__()
        self.sql_account = sql_file.UsersSql()
        self.sql_account.create_current_user_db()

        self.account_window = self

        user = self.sql_account.cur.execute("SELECT * FROM current_user").fetchone()
        id = user[0]
        username = user[1]
        password = user[2]

        self.account_window.title(f"{username.title()} Account")
        ICON_2 = tkinter.PhotoImage(file="images_icons/leaf.png")
        self.account_window.iconphoto(False, ICON_2)

        self.account_window.config(pady=10, padx=20, bg="white")

        username_text_info = tkinter.Label(master=self.account_window, text=f"""
            USERNAME: {username.title()}

            PASSWORD: {password}

            USER ID: {id}
            """, bg="white", padx=5)
        username_text_info.grid(column=0, row=0)

        canvas_ac = tkinter.Canvas(master=self.account_window, width=150, height=150, bg="white", highlightthickness=0)
        image_ac = tkinter.PhotoImage(master=self.account_window, file="images_icons/user.png")
        canvas_ac.create_image(80, 70, image=image_ac)
        canvas_ac.grid(column=1, row=0)

        self.account_window.mainloop()
