# %%
import spacy
import neuralcoref
from spacy import matcher
from spacy.matcher import Matcher

nlp = spacy.load("en_core_web_sm")
neuralcoref.add_to_pipe(nlp)


text = (
    "ACR will use ADW as a source. It is a reporting tool and it uses Aladdin Enterprise as a source. Paul Huizinga works with it. He is a data architect for Aegon Asset Management")


class coreference():
    def __init__(self):
        pass

    def get_neuralcoref_entities(self, in_text):
        """
        Unicode representation of the doc where each corefering mention is replaced by the main mention in the associated cluster.
        """
        doc = nlp(in_text)
        out_text = doc._.coref_resolved

        return out_text


class named_entity_recognition():
    """
    nouns and proper nouns are entities

    """
    def __init__(self):
        pass

    def print_spacy_entities(self, text):
        doc = nlp(text)
        print('PRINTING SPACY ENTITIES')
        print('-' * 50)

        for entity in doc.ents:
            print(entity.text, entity.label_)

    def get_entities(self, text):
        doc = nlp(text)
        return set([chunk.text for chunk in doc.noun_chunks])

class text_exploration():
    def __init__(self):
        pass

    def print_token_dependency_pos(self, text):
        """
        print token, dependency, POS (parts-of-speech) tag
        """
        for tok in doc:
            print(tok.text, "-->", tok.dep_, "-->", tok.pos_)

a = coreference().get_neuralcoref_entities(text)
b = named_entity_recognition().get_entities(a)
print(b)
named_entity_recognition().print_spacy_entities(a)

# %%
# Neuralcoref options
doc = nlp(u'My sister has a dog. She loves him.')

# All the clusters of corefering mentions in the doc
print('All the clusters of corefering mentions in the doc')
print(doc._.coref_clusters)
print(doc._.coref_clusters[1].mentions)
print(doc._.coref_clusters[1].mentions[-1]._.coref_cluster.main)

# Unicode representation of the doc where each corefering mention is replaced by the main mention in the associated cluster.
print(
    'Unicode representation of the doc where each corefering mention is replaced by the main mention in the associated cluster.')
print(doc._.coref_resolved)

# Scores of the coreference resolution between mentions.
print('Scores of the coreference resolution between mentions.')
print(doc._.coref_scores)

span = doc[-1:]
# 	Whether the span has at least one corefering mention
print('	Whether the span has at least one corefering mention')
print(span._.is_coref)
# print(span._.coref_cluster.main)
# print(span._.coref_cluster.main._.coref_cluster)

token = doc[-1]
print(token._.in_coref)
print(token._.coref_clusters)


# %%
# all tokens in dict
def create_dict_of_text(doc):
    """
    create a dictionary of a spacy document. The dict will include the text, the word type and the ??
    :param doc: spacy document
    :return: dictionairy
    """
    loc = 0
    text_dict = {}
    for token in doc:
        text_dict[loc] = {'text': token.text, 'pos_': token.pos_, 'dep_': token.dep_}
        loc += 1

    return text_dict


def merge_propn_and_noun(d):
    keys_to_be_removed = []
    for k, v in d.items():
        if k > 0 and d[k]['pos_'] == "PROPN" and d[k - 1]['pos_'] == "PROPN":
            d[k]['text'] = str(d[k - 1]['text']) + ' ' + str(d[k]['text'])
            keys_to_be_removed.append(k - 1)
        if k > 0 and d[k]['pos_'] == "NOUN" and d[k]['dep_'] == "attr" and d[k - 1]['pos_'] == "NOUN":
            d[k]['text'] = str(d[k - 1]['text']) + ' ' + str(d[k]['text'])
            keys_to_be_removed.append(k - 1)
        if k > 0 and d[k]['pos_'] == "NOUN" and d[k]['dep_'] == "dobj" and d[k - 1]['pos_'] == "VERB":
            d[k]['text'] = str(d[k - 1]['text']) + ' ' + str(d[k]['text'])
            keys_to_be_removed.append(k - 1)
    # remove keys
    remove_keys_from_dict(keys_to_be_removed, d)

    return d


def co_reference(d):
    last_subj = ''
    pre_last_subj = ''
    for k, v in d.items():
        # replace co-reference with the subject
        if d[k]['pos_'] == "PRON" and d[k]['dep_'] == "pobj" and last_subj != '':
            d[k]['text'] = pre_last_subj
        if d[k]['pos_'] == "PRON" and last_subj != '':
            d[k]['text'] = last_subj
        # get the last subject
        if d[k]['dep_'] == 'nsubj':
            pre_last_subj = last_subj
            last_subj = d[k]['text']

    return d


def remove_unused_words_from_dict(d):
    keys_to_be_removed = []
    for k, v in d.items():
        if d[k]['pos_'] == 'AUX' and d[k]['dep_'] != 'ROOT':
            keys_to_be_removed.append(k)
        if d[k]['pos_'] == 'DET':
            keys_to_be_removed.append(k)

    remove_keys_from_dict(keys_to_be_removed, d)

    return d


# remove non useable keys
def remove_keys_from_dict(lst, d):
    for key in lst:
        del d[key]

    return d


def create_adjusted_text(d):
    text = []
    t = ''

    for k, v in d.items():
        text.append(d[k]['text'])

    for a in text:
        t = t + ' ' + a

    return t


def print_spacy_word_characteristics(text):
    doc = nlp(text)
    print('PRINTING SPACY WORD CHARACTERISTICS')
    print('-' * 50)

    for token in doc:
        print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
              token.shape_, token.is_alpha, token.is_stop)


def get_relations(text):
    doc = nlp(text)
    entities = get_entities(text)

    for sent in doc.sents:
        for ent in entities:
            if ent in str(sent):
                print(ent, sent)


# %%

a = create_dict_of_text(doc)
b = merge_propn_and_noun(a)
c = co_reference(b)
d = remove_unused_words_from_dict(c)
e = create_adjusted_text(d)
print_spacy_entities(text)
print_spacy_entities(e)
f = get_entities(text)
g = get_entities(e)

# %%

doc2 = nlp(e)
print("Noun phrases:", set([chunk.text for chunk in doc2.noun_chunks]))
print("Verbs:", set([token.lemma_ for token in doc if token.pos_ == "VERB"]))
# %%
import spacy

# Load English tokenizer, tagger, parser and NER
nlp = spacy.load("en_core_web_sm")
# Load Dutch tokenizer, tagger, parser and NER
# nlp = spacy.load("nl_core_news_sm")


# %%
text = (
    "ACR will use ADW as a source. It is a reporting tool and it uses Aladdin Enterprise as a source. Paul works with it. He is a data architect for Aegon Asset Management")

# doc = nlp(text3)
doc = nlp(text)

# Analyze syntax
print("Noun phrases:", set([chunk.text for chunk in doc.noun_chunks]))
# print("Verbs:", set([token.lemma_ for token in doc if token.pos_ == "VERB"]))

# Find named entities, phrases and concepts
for entity in doc.ents:
    print(entity.text, entity.label_)

print("-" * 30)

# get all word characteristics
for token in doc:
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
          token.shape_, token.is_alpha, token.is_stop)

# %%
spacy.explain("dobj")
# %%
# visualize sentence (works only in jupyter (i think...))
from spacy import displacy

displacy.render([doc], style="dep", minify=True)
