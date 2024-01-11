import pandas as pd

# Vegetable data
vegetable_data = [
    {"Vegetable": "Carrot", "Color": "Orange"},
    {"Vegetable": "Broccoli", "Color": "Green"},
    {"Vegetable": "Tomato", "Color": "Red"},
    {"Vegetable": "Cucumber", "Color": "Green"},
    {"Vegetable": "Eggplant", "Color": "Purple"},
    {"Vegetable": "Bell Pepper", "Color": "Red"},
    {"Vegetable": "Spinach", "Color": "Green"},
    {"Vegetable": "Beetroot", "Color": "Purple"},
    {"Vegetable": "Cauliflower", "Color": "White"},
    {"Vegetable": "Lettuce", "Color": "Green"}
]

# Create a DataFrame
df = pd.DataFrame(vegetable_data)

# Display the DataFrame
print(df)

