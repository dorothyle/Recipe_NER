import spacy
from spacy import displacy

nlp = spacy.load('en_core_web_sm')
doc = nlp(u'This is a sentence')
doc = nlp(u'Rats are various medium-sized, long-tailed rodents.')
displacy.serve(doc, style='ent', port=5050)
