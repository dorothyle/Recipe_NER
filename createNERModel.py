import spacy
from TASTEset.src.utils import prepare_data, ENTITIES

print("hello world!")
recipes, entities = prepare_data("TASTEset/data/TASTEset.csv")
print(recipes[0])
print(ENTITIES)
print(entities[0])
print([f"{recipes[0][start:end]}: {ent}" for start, end, ent in entities[0]])

annotations = [{'text': ' '.join(recipe.splitlines()), 'entities': ents} for recipe, ents in zip(recipes, entities)]
training_data = {'classes': ENTITIES, 'annotations': annotations}

from spacy.tokens import DocBin

nlp = spacy.blank("en")

def doc_from_annotations(annotations):

  doc_bin = DocBin()

  for example in annotations:
    doc = nlp.make_doc(example['text'])
    ents = []
    for entity in example['entities']:
      span = doc.char_span(*entity)
      ents.append(span)

    doc.ents = ents
    doc_bin.add(doc)
  return doc_bin

train_len = int(0.8*len(annotations))
print("training length=", train_len)

train_bin = doc_from_annotations(annotations[:train_len])
dev_bin = doc_from_annotations(annotations[train_len:])

train_bin.to_disk("nerfr_train.spacy")
dev_bin.to_disk("nerfr_dev.spacy")
