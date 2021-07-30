# pip install -U spacy
# python -m spacy download en_core_web_sm
# python -m spacy download nl_core_news_sm
import neuralcoref
# %%
# function to handle co-reference (replace 'he', 'it', etc)
# also remove unused words
# also combine pronouns and nouns (if applicable)
import spacy

# Load English tokenizer, tagger, parser and NER
nlp = spacy.load("en_core_web_sm")

text = (
    """Why You Should Care about Graph Databases
New tech is great, but you operate in a world of budgets, timelines, corporate standards and competitors. You don’t merely replace
your existing database infrastructure just because something new comes along – you only take action when an orders-of-magnitude
improvement is at hand.
Graph databases fit that bill, and here’s why:
Performance
Your data volume will definitely increase in the future, but what’s going to increase at an even faster clip is the connections (or
relationships) between your individual data points. With traditional databases, relationship queries (also known as “JOINs”) will come to
a grinding halt as the number and depth of relationships increase. In contrast, graph database performance stays consistent even as
your data grows year over year.
Flexibility
With graph databases, your IT and data architect teams move at the speed of business because the structure and schema of a graph
data model flex as your solutions and industry change. Your team doesn’t have to exhaustively model your domain ahead of time;
instead, they can add to the existing structure without endangering current functionality.
Agility
Developing with graph databases aligns perfectly with today’s agile, test-driven development practices, allowing your graph-databasebacked application to evolve alongside your changing business requirements.
What Is a Graph Database? (A Non-Technical Definition)
You don’t need to understand the arcane mathematical wizardry
of graph theory in order to understand graph databases. On the
contrary, they’re more intuitive to understand than relational database
management systems (RDBMS).
A graph is composed of two elements: a node and a relationship. Each
node represents an entity (a person, place, thing, category or other
piece of data), and each relationship represents how two nodes are
associated. For example, the two nodes “cake” and “dessert” would
have the relationship “is a type of” pointing from “cake” to “dessert.”
Twitter is a perfect example of a graph database connecting 313 million
monthly active users. In the illustration to the right, we have a small
slice of Twitter users represented in a graph data model.
Each node (labeled “User”) belongs to a single person and is connected
with relationships describing how each user is connected. As we
can see, Billy and Harry follow each other, as do Harry and Ruth, but
although Ruth follows Billy, Billy hasn’t (yet) reciprocated.
If the above example makes sense to you, then you’ve already grasped
the basics of what makes up a graph database""")

text = (
    "ACR will use ADW as a source. It is a reporting tool and it uses Aladdin Enterprise as a source. Paul works with it. He is a data architect for Aegon Asset Management")

doc = nlp(text)


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


def print_spacy_entities(text):
    doc = nlp(text)
    print('PRINTING SPACY ENTITIES')
    print('-' * 50)

    for entity in doc.ents:
        print(entity.text, entity.label_)


def get_entities(text):
    doc = nlp(text)
    return set([chunk.text for chunk in doc.noun_chunks])


def get_relations(text):
    doc = nlp(text)
    entities = get_entities(text)

    for sent in doc.sents:
        for ent in entities:
            if ent in str(sent):
                print(ent, sent)




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
#%%
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