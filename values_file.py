import random

# Different values that we use in the program
# Humidity, sunlight and pH are randomly generated

HUMIDITY = random.randint(1, 10)
SUNLIGHT = random.randint(1, 10)
PH_VALUE = round(random.uniform(4.3, 6.5), 2)

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

def image_to_sql(photo_input):
    with open(photo_input, 'rb') as x:
        return x.read()

STARTING_PLANTS = [
    (1, 'Rosemary', 'Kitchen', HUMIDITY, PH_VALUE, SUNLIGHT, image_to_sql('plants_photos/Rosemary.jpg'), 'No notes'),
    (2, 'Basil', 'Kitchen', HUMIDITY, PH_VALUE, SUNLIGHT, image_to_sql('plants_photos/Basil.jpg'), 'No notes'),
    (3, 'Peas', 'Back garden', HUMIDITY, PH_VALUE, SUNLIGHT, image_to_sql('plants_photos/Peas.jpg'), 'No notes'),
    (4, 'Carrot', 'Back garden', HUMIDITY, PH_VALUE, SUNLIGHT, image_to_sql('plants_photos/Carrot.jpg'), 'No notes'),
    (5, 'Spinach', 'Back garden', HUMIDITY, PH_VALUE, SUNLIGHT, image_to_sql('plants_photos/Spinach.jpg'), 'No notes'),
    (6, 'Parsley', 'Kitchen', HUMIDITY, PH_VALUE, SUNLIGHT, image_to_sql('plants_photos/Parsley.jpg'), 'No notes'),
    (7, 'Pepper', 'Back garden', HUMIDITY, PH_VALUE, SUNLIGHT, image_to_sql('plants_photos/Pepper.jpg'), 'No notes'),
    (8, 'Cactus', 'Living room', HUMIDITY, PH_VALUE, SUNLIGHT, image_to_sql('plants_photos/Cactus.jpg'), 'No notes'),
    (9, 'Habanero', 'Kitchen', HUMIDITY, PH_VALUE, SUNLIGHT, image_to_sql('plants_photos/Habanero.jpg'), 'No notes'),
    (10, 'Bonsai', 'Living room', HUMIDITY, PH_VALUE, SUNLIGHT, image_to_sql('plants_photos/Bonsai.jpg'), 'No notes'),
]


def humidity_to_text(humidity_input):
    if humidity_input <= 3:
        humidity_text = "Low, needs watering"
    elif humidity_input >= 4 and humidity_input <= 8:
        humidity_text = "Average"
    else:
        humidity_text = "High"
    return humidity_text


def sunlight_to_text(sunlight_input):
    if sunlight_input <= 3:
        sunlight_text = "Low"
    elif sunlight_input >= 4 and sunlight_input <= 8:
        sunlight_text = "Medium"
    else:
        sunlight_text = "High"
    return sunlight_text

