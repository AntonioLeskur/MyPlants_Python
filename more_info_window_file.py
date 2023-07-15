import sql_file
import random
import tkinter
from PIL import Image

# Window that contains plant info and grapg


class MoreInfoWindow(tkinter.Toplevel):

    def __init__(self, listbox_plant):
        import values_file
        super().__init__()
        self.sql_more_info_w = sql_file.PlantSql()
        self.PLANT_NAME_info = listbox_plant
        self.HUMIDITY_info = random.randint(1, 10)
        self.HUMIDITY_text = values_file.humidity_to_text(self.HUMIDITY_info)
        self.SUNLIGHT_info = random.randint(1, 10)
        self.SUNLIGHT_text = values_file.sunlight_to_text(self.SUNLIGHT_info)
        self.PH_VALUE_info = round(random.uniform(4.3, 6.5), 2)

        self.info_window = self
        self.info_window.title(f"{self.PLANT_NAME_info}")
        self.info_window.config(pady=10, padx=20, bg="white")
        self.ICON_2 = tkinter.PhotoImage(file="images_icons/leaf.png")
        self.info_window.iconphoto(False, self.ICON_2)


        PLANT = self.sql_more_info_w.c.execute(f'SELECT * FROM plants WHERE plant_name="{self.PLANT_NAME_info}"').fetchone()

        plant_info = tkinter.Label(master=self.info_window, text=f"""
            Plant: {PLANT[1]}
    
            Plant ID: {PLANT[0]}
    
            Plant location: {PLANT[2]}
    
            Note: {PLANT[7]}
            """, bg="white")
        plant_info.grid(column=0, row=0)

        @staticmethod
        def sql_to_photo(plant_name):
            from_db = self.sql_more_info_w.c.execute(f'SELECT * FROM plants WHERE plant_name="{plant_name}"').fetchall()
            for pl in from_db:
                bin = pl[6]
            with open("images_icons/image_holder.jpg", 'wb') as x:
                x.write(bin)
            png = Image.open(r'images_icons/image_holder.jpg')
            png.save(r'images_icons/image_holder.png')

        sql_to_photo(self.PLANT_NAME_info)

        self.canvas = tkinter.Canvas(master=self.info_window, width=210, height=350, bg="white", highlightthickness=0)
        self.image = tkinter.PhotoImage(file="images_icons/image_holder.png", master=self.info_window)
        self.canvas.create_image(50, 150, image=self.image)
        self.canvas.grid(column=1, row=0)

        self.graph_button = tkinter.Button(master=self.info_window, text=f"{self.PLANT_NAME_info} graph", width=13,
                                           bg="#FFFFFF", bd=1, command=self.graph
                                           )
        self.graph_button.grid(column=0, row=1, columnspan=2)

    def graph(self):
        import matplotlib.pyplot as plt
        from matplotlib.figure import Figure
        labels = [f"HUMIDITY: {self.HUMIDITY_text}", f"SUNLIGHT: {self.SUNLIGHT_text}", f"pH: {self.PH_VALUE_info} pH"]
        colors = ["#79E0EE", "#FFD93D", "#54B435"]
        plt.pie([self.HUMIDITY_info, self.SUNLIGHT_info, self.PH_VALUE_info], labels=labels, colors=colors)

        fig = Figure(figsize=(5, 7), dpi=100)
        ax = fig.add_subplot(111)
        plt.show()

