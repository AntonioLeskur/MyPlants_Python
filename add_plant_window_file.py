import tkinter
from tkinter import messagebox

# Window for adding a new plant


class AddPlant(tkinter.Toplevel):
    def __init__(self):
        super().__init__()
        ICON = tkinter.PhotoImage(file="images_icons/leaf.png")
        self.add_plant_window = self
        self.add_plant_window.title("Add Plant")
        self.add_plant_window.config(pady=10, padx=20, bg="white")
        self.add_plant_window.iconphoto(False, ICON)

        self.canvas_add = tkinter.Canvas(master=self.add_plant_window, width=150, height=150, bg="white",
                                         highlightthickness=0
                                         )
        self.image_add = tkinter.PhotoImage(master=self.add_plant_window, file="images_icons/dirt.png")
        self.canvas_add.create_image(75, 70, image=self.image_add)
        self.canvas_add.grid(column=1, row=0, columnspan=2, sticky="W")

        add_name_text = tkinter.Label(master=self.add_plant_window, text="Plant:", bg="white")
        add_name_text.grid(sticky="E", column=0, row=1)

        self.add_name_entry = tkinter.Entry(master=self.add_plant_window, width=33)
        self.add_name_entry.grid(sticky="W", column=1, row=1, columnspan=2)

        add_location_text = tkinter.Label(master=self.add_plant_window, text="Plant location:", bg="white")
        add_location_text.grid(sticky="E", column=0, row=2)

        self.add_location_entry = tkinter.Entry(master=self.add_plant_window, width=33)
        self.add_location_entry.grid(sticky="W", column=1, row=2, columnspan=2)

        add_note_text = tkinter.Label(master=self.add_plant_window, text="Note:", bg="white")
        add_note_text.grid(sticky="E", column=0, row=3)

        self.add_note_entry = tkinter.Entry(master=self.add_plant_window, width=33)
        self.add_note_entry.grid(sticky="W", column=1, row=3, columnspan=2)

        add_new_plant_button = tkinter.Button(master=self.add_plant_window, text="Add", width=15, bg="#FFFFFF", bd=1,
                                              command=self.submit_plant)
        add_new_plant_button.grid(sticky="W", column=1, row=4, columnspan=2, pady=3)

    def submit_plant(self):
        import sql_file
        import values_file
        sql_add_plants = sql_file.PlantSql()

        SUBMIT_PLANT = """INSERT INTO plants 
        (plant_name, plant_location, plant_humidity, ph, plant_sunlight, plant_photo, plant_notes) 
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """
        plant_name = self.add_name_entry.get()
        location = self.add_location_entry.get()
        notes = self.add_note_entry.get()
        with sql_add_plants.conn_plants:
            sql_add_plants.conn_plants.execute(SUBMIT_PLANT, (
                plant_name, location, values_file.HUMIDITY, values_file.PH_VALUE, values_file.SUNLIGHT,
                values_file.image_to_sql('images_icons/no_photo_plant.png'), notes))
            sql_add_plants.conn_plants.commit()
        tkinter.messagebox.showinfo(title=plant_name, message=f"Plant: {plant_name}, has been added.")
        self.add_plant_window.destroy()
