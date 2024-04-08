from recipe_scrapers import scrape_me

RECIPE_URL = "https://www.allrecipes.com/recipe/246868/pecan-sour-cream-coffee-cake/"
scraper = scrape_me(RECIPE_URL)
print(scraper.ingredients())

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


def process_text(text):
  """
  A wrapper function to pre-process text and run it through our pipeline.
  """
  return nlp(convert_floats_to_fractions(text))

# Checks conversion of floats to fractions
print([convert_floats_to_fractions(line) for line in scraper.ingredients()])
