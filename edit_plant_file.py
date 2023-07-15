import tkinter
from tkinter import messagebox
import sql_file

# Edit an already existing plant


class Edit(tkinter.Toplevel):
    def __init__(self, listbox):
        super().__init__()
        self.LISTBOX = listbox
        PLANT_NAME = self.LISTBOX.get(tkinter.ANCHOR)
        self.PLANT = sql_file.PlantSql().c.execute(f'SELECT * FROM plants WHERE plant_name="{PLANT_NAME}"').fetchone()
        self.edit_window = self
        self.edit_window.frame()
        self.edit_window.title(f"Edit {PLANT_NAME}")
        ICON_2 = tkinter.PhotoImage(file="images_icons/leaf.png")
        self.edit_window.iconphoto(False, ICON_2)

        self.edit_window.config(pady=10, padx=20, bg="white")

        plant_info = tkinter.Label(master=self.edit_window, text=f"""
                Plant: {self.PLANT[1]}  |  Plant ID: {self.PLANT[0]}
    
                Plant location: {self.PLANT[2]}  |  Note: {self.PLANT[7]}
                """, bg="white")
        plant_info.grid(column=0, row=0, columnspan=2)

        plant_name_text = tkinter.Label(text="Plant:", bg="white", master=self.edit_window)
        plant_name_text.grid(sticky="E", column=0, row=1)

        self.plant_name_entry = tkinter.Entry(width=45, master=self.edit_window)
        self.plant_name_entry.insert(0, PLANT_NAME)
        self.plant_name_entry.grid(sticky="W", column=1, row=1, columnspan=1)

        plant_location_text = tkinter.Label(text="Plant location:", bg="white", master=self.edit_window)
        plant_location_text.grid(sticky="E", column=0, row=2)

        self.plant_location__entry = tkinter.Entry(width=45, master=self.edit_window)
        self.plant_location__entry.insert(0, self.PLANT[2])
        self.plant_location__entry.grid(sticky="W", column=1, row=2, columnspan=1)

        notes_text = tkinter.Label(text="Note:", bg="white", master=self.edit_window)
        notes_text.grid(sticky="E", column=0, row=3)

        self.notes_entry = tkinter.Text(width=35, height=15, master=self.edit_window)
        self.notes_entry.insert(1.0, self.PLANT[7])
        self.notes_entry.grid(sticky="W", column=1, row=3)

        submit_button = tkinter.Button(text="Submit", width=13, bg="#FFFFFF", bd=1, master=self.edit_window,
                                       command=self.submit
                                       )
        submit_button.grid(column=0, row=4, columnspan=2)

    def submit(self):
        sql_edit_plant = sql_file.PlantSql()
        notes = self.notes_entry.get(1.0, tkinter.END)
        plant = self.plant_name_entry.get()
        location = self.plant_location__entry.get()
        sql_edit_plant.c.execute(f"UPDATE plants SET plant_name = '{plant}' WHERE id = {self.PLANT[0]}")
        sql_edit_plant.c.execute(f"UPDATE plants SET plant_location = '{location}' WHERE id = {self.PLANT[0]}")
        sql_edit_plant.c.execute(f"UPDATE plants SET plant_notes = '{notes}' WHERE id = {self.PLANT[0]}")
        sql_edit_plant.conn_plants.commit()
        self.LISTBOX.delete(0, tkinter.END)
        sql_edit_plant.c.execute("SELECT * FROM plants")
        sql_edit_plant.c.fetchall()
        self.edit_window.destroy()
        tkinter.messagebox.showinfo(title="Plant updated", message=f"{self.PLANT[1]} is updated.")
