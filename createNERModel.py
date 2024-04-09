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

# Base config for efficiency optimization

# This is an auto-generated partial config. To use it with 'spacy train'
# you can run spacy init fill-config to auto-fill all default settings:
# python -m spacy init fill-config ./base_config.cfg ./config.cfg
BASE_CONFIG = """[paths]
train = nerfr_train.spacy
dev = nerfr_dev.spacy
vectors = null
[system]
gpu_allocator = null

[nlp]
lang = "en"
pipeline = ["tok2vec","ner"]
batch_size = 1000

[components]

[components.tok2vec]
factory = "tok2vec"

[components.tok2vec.model]
@architectures = "spacy.Tok2Vec.v2"

[components.tok2vec.model.embed]
@architectures = "spacy.MultiHashEmbed.v2"
width = ${components.tok2vec.model.encode.width}
attrs = ["NORM", "PREFIX", "SUFFIX", "SHAPE"]
rows = [5000, 1000, 2500, 2500]
include_static_vectors = false

[components.tok2vec.model.encode]
@architectures = "spacy.MaxoutWindowEncoder.v2"
width = 96
depth = 4
window_size = 1
maxout_pieces = 3

[components.ner]
factory = "ner"

[components.ner.model]
@architectures = "spacy.TransitionBasedParser.v2"
state_type = "ner"
extra_state_tokens = false
hidden_width = 64
maxout_pieces = 2
use_upper = true
nO = null

[components.ner.model.tok2vec]
@architectures = "spacy.Tok2VecListener.v1"
width = ${components.tok2vec.model.encode.width}

[corpora]

[corpora.train]
@readers = "spacy.Corpus.v1"
path = ${paths.train}
max_length = 0

[corpora.dev]
@readers = "spacy.Corpus.v1"
path = ${paths.dev}
max_length = 0

[training]
dev_corpus = "corpora.dev"
train_corpus = "corpora.train"

[training.optimizer]
@optimizers = "Adam.v1"

[training.batcher]
@batchers = "spacy.batch_by_words.v1"
discard_oversize = false
tolerance = 0.2

[training.batcher.size]
@schedules = "compounding.v1"
start = 100
stop = 1000
compound = 1.001

[initialize]
vectors = ${paths.vectors}
"""

with open("base_config.cfg", 'w') as f:
  f.write(BASE_CONFIG)