import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import SnowballStemmer  # voor het verkorten van woorden naar de stam
import logging


# spacy library bekijken

dutch_stemmer = SnowballStemmer('dutch')  # voor Nederlands

nltk.download('stopwords')
nltk.download('punkt')

# LOGGING
logger = logging.getLogger(__name__)  # initialize logger
logger.handlers = []
c_handler = logging.StreamHandler()  # Create handlers
c_format = logging.Formatter('%(levelname)s - %(message)s')
c_handler.setFormatter(c_format)  # Create formatters and add it to handlers
logger.addHandler(c_handler)  # Add handlers to the logger
logger.setLevel(logging.DEBUG)

with open('familytree.txt', encoding="utf8") as f:
    content = f.readlines()

# remove whitespace characters like `\n` at the end of each line
tot = [x.strip() for x in content]

# all text in string
all_txt_in_one = ''
for x in tot:
    all_txt_in_one = all_txt_in_one + x

# actual logging
logger.debug('number of items in y: {}'.format(len(all_txt_in_one)))

# add a space after each point
lst = list(all_txt_in_one)
for i, s in enumerate(lst):
    if s == '.':
        lst.insert(i + 1, ' ')

# all text in string
all_txt_in_one = ''
for x in lst:
    all_txt_in_one = all_txt_in_one + x

# sentence tokenizer
sentences = sent_tokenize(all_txt_in_one)
words = word_tokenize(all_txt_in_one)

print('number of sentences: {}'.format(len(sentences)))
print('number of words: {}'.format(len(words)))

# remove stopwords
clean_words = words[:]
sr = stopwords.words('dutch')
for word in words:
    if word in stopwords.words('dutch'):
        clean_words.remove(word)

print('number of clean_words: {}'.format(len(clean_words)))

# plot the 20 most frequent words
freq = nltk.FreqDist(clean_words)
freq.plot(20, cumulative=False)

for i, w in enumerate(clean_words):
    if w == 'overleden' or w == 'overleed' or w == 'geboren':
        print(clean_words[i -3:i + 3])
