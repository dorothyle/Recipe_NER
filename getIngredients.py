import spacy
# Load model
nlp = spacy.load("output_eff/model-best")

from recipe_scrapers import scrape_me

RECIPE_URL = "https://www.allrecipes.com/recipe/246868/pecan-sour-cream-coffee-cake/"
scraper = scrape_me(RECIPE_URL)
# print(scraper.ingredients()) # Prints ingredients scraped from website

# Convert quantities as fractions
from fractions import Fraction
import re


def fraction_to_mixed_number(fraction: Fraction) -> str:
  if fraction.numerator >= fraction.denominator:
    whole, remainder = divmod(fraction.numerator, fraction.denominator)
    if remainder == 0:
      return str(whole)
    else:
      return f"{whole} {Fraction(remainder, fraction.denominator)}"
  else:
    return str(fraction)


def convert_floats_to_fractions(text: str) -> str:
    return re.sub(
        r'\b-?\d+\.\d+\b',
        lambda match: fraction_to_mixed_number(
            Fraction(float(match.group())).limit_denominator()), text
        )


# Recieves an ingredient and returns 1 or more food entities
def process_ingredient(ingredient):
    """
    A wrapper function to pre-process ingredient and run it through our pipeline.
    """
    doc = nlp(convert_floats_to_fractions(ingredient))
    food_entities = []
    for ent in doc.ents:
       if ent.label_ == "FOOD":
          food_entities.append(ent.text)
    return food_entities

# Checks conversion of floats to fractions
# print([convert_floats_to_fractions(line) for line in scraper.ingredients()])

from spacy import displacy
# process the recipe, line-by-line
def cleanIngredients(uncleaned_ingredients):
  ingredient_list = set()
  for line in uncleaned_ingredients:
    foods = process_ingredient(line)
    ingredient_list.update(foods)
  return list(ingredient_list)
