import csv
from getIngredients import *

# open file to read
original_file = open('Food Ingredients and Recipe Dataset with Image Name Mapping.csv')
reader = csv.reader(original_file)
# TODO: open file to write to
# cleaned_file = open('CLEANED Dataset.csv', 'w')
# writer = csv.writer(cleaned_file)

# iterate through file to read
i = 0
for row in reader:
    if i != 0:
        # extract uncleaned ingredients into list
        uncleaned_ingredients = row[5][2:-2].split("', '")
        print("UNCLEANED:", uncleaned_ingredients)

        # receive cleaned ingredients with NER
        cleaned_ingredients = cleanIngredients(uncleaned_ingredients)
        print("CLEANED:", cleaned_ingredients)
        print()
        # TODO: append cleaned ingredients to row
    # TODO: add each row to new file
    i += 1
    if i == 8:
        break