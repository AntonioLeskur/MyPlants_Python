import tkinter
import sql_file
from tkinter import messagebox
import account_window_info_file
import add_plant_window_file

# Main window

class MainWindow(tkinter.Tk):

    def __init__(self):
        super().__init__()
        self.sql_main_window_users = sql_file.UsersSql()
        self.sql_main_window_users.create_current_user_db()

        self.sql_main_window_plants = sql_file.PlantSql()
        self.sql_main_window_plants.create_plant_table()

        self.window_main = self
        self.window_main.title("MyPlants")
        self.window_main.config(pady=10, padx=20, bg="white")
        ICON_2 = tkinter.PhotoImage(file="images_icons/leaf.png", master=self.window_main)
        self.window_main.iconphoto(False, ICON_2)

        # Checking if logged user is admin

        user = self.sql_main_window_users.cur.execute("SELECT * FROM current_user").fetchone()
        username = user[1]
        password = user[2]
        if username == "Admin" and password == "admin":
            ADMIN = True
        else:
            ADMIN = False

        plants_button = tkinter.Button(text="Refresh list", width=13, bg="#FFFFFF", bd=1, command=self.show_plants)
        plants_button.grid(column=0, row=0)

        my_account_button = tkinter.Button(text="My_account", width=13, bg="#FFFFFF", bd=1,
                                           command=account_window_info_file.AccountInfo
                                           )
        my_account_button.grid(column=1, row=0)

        log_out_button = tkinter.Button(text="Log Out", width=13, bg="#FFFFFF", bd=1, command=self.log_out)
        log_out_button.grid(column=2, row=0)

        self.search_entry = tkinter.Entry(self.window_main, width=45)
        self.search_entry.bind("<KeyRelease>", func=self.window_main.search_plants)
        self.search_entry.grid(column=0, row=1, columnspan=2)

        search_label = tkinter.Label(text=": Searched Item", width=13, bg="#FFFFFF", bd=1)
        search_label.grid(sticky="W", column=2, row=1)

        self.listbox_data = tkinter.Listbox(master=self.window_main)
        self.listbox_data.grid(column=0, row=2, columnspan=2, pady=5)
        self.listbox_data.config(width=40, height=20)

        more_info_button = tkinter.Button(text="More info", width=13, bg="#FFFFFF", bd=1, command=self.show_more_info)
        more_info_button.grid(column=0, row=3)

        add_plant_button = tkinter.Button(text="Add plant", width=13, bg="#FFFFFF", bd=1,
                                          command=add_plant_window_file.AddPlant
                                          )
        add_plant_button.grid(sticky="W", column=1, row=3)

        canvas = tkinter.Canvas(width=120, height=350, bg="white", highlightthickness=0)
        image = tkinter.PhotoImage(file="images_icons/plant.png")
        canvas.create_image(100, 200, image=image)
        canvas.grid(column=2, row=2, padx=2, columnspan=2)

        # Only admin can edit or delete

        if ADMIN:
            edit_button = tkinter.Button(text="Edit", width=13, bg="#FFFFFF", bd=1, command=self.edit_plant)
            edit_button.grid(sticky="W", column=2, row=3)
        else:
            edit_button = tkinter.Button(text="Edit", width=13, bg="#B0A4A4", bd=1, command=self.no_admin_massage)
            edit_button.grid(sticky="W", column=2, row=3)

        if ADMIN:
            delete_button = tkinter.Button(text="Delete", width=13, bg="#FFFFFF", bd=1, command=self.delete)
            delete_button.grid(sticky="W", column=3, row=3, padx=15)
        else:
            delete_button = tkinter.Button(text="Delete", width=13, bg="#B0A4A4", bd=1, command=self.no_admin_massage)
            delete_button.grid(sticky="W", column=3, row=3, padx=15)

        self.window_main.mainloop()

    def log_out(self):
        from log_in_window_file import LogInWindow
        self.window_main.destroy()
        LogInWindow()

    def no_admin_massage(self):
        tkinter.messagebox.showerror(title="Only Admin", message="Only admins can do that.")

    def show_plants(self):
        self.sql_main_window_plants = sql_file.PlantSql()
        self.sql_main_window_plants.c.execute("SELECT * FROM plants")
        plants_table_all = self.sql_main_window_plants.c.fetchall()
        self.listbox_data.delete(0, tkinter.END)
        for x in range(len(plants_table_all)):
            self.listbox_data.insert(tkinter.END, plants_table_all[x][1])

    def show_more_info(self):
        import more_info_window_file
        plant_name = self.listbox_data.get(tkinter.ANCHOR)
        if plant_name == "":
            tkinter.messagebox.showinfo(title="No plant selected", message="No plant selected")
        else:
            more_info_window_file.MoreInfoWindow(plant_name)

    def edit_plant(self):
        import edit_plant_file
        plant_name = self.listbox_data.get(tkinter.ANCHOR)
        if plant_name == "":
            tkinter.messagebox.showinfo(title="No plant selected", message="No plant selected")
        else:
            edit_plant_file.Edit(self.listbox_data)

    def delete(self):
        plant_name = self.listbox_data.get(tkinter.ANCHOR)
        if plant_name == "":
            tkinter.messagebox.showinfo(title="No plant selected", message="No plant selected")
        else:
            do_delete = tkinter.messagebox.askokcancel(title="DELETE",
                                                       message=f"Are you sure you want to delete {plant_name} ?")
            if do_delete:
                self.listbox_data.delete(tkinter.ANCHOR)
                self.sql_main_window_plants.conn_plants.execute(f"DELETE FROM plants WHERE plant_name = '{plant_name}'")
                self.sql_main_window_plants.conn_plants.commit()

    def update_listbox(self, data):
        self.listbox_data.delete(0, tkinter.END)
        for item in data:
            self.listbox_data.insert(tkinter.END, item)

    def search_plants(self, event):
        self.sql_main_window_plants.c.execute("SELECT * FROM plants")
        plants_table_all = self.sql_main_window_plants.c.fetchall()
        plant_names = [plants_table_all[x][1] for x in range(len(plants_table_all))]
        print(plant_names)
        typed = self.search_entry.get()
        if typed == "":
            data = plant_names
        else:
            data = []
            for item in plant_names:
                if typed.title() in item.title():
                    data.append(item)
        self.update_listbox(data)

