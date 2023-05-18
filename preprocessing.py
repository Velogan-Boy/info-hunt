import nltk
import json
from nltk.corpus import stopwords
from nltk import ngrams
from nltk import ToktokTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.corpus import wordnet
import pickle
import sklearn
from sklearn.metrics.pairwise import cosine_similarity

# Download all the required files
nltk.download('stopwords')  # downloads stopword
nltk.download('wordnet')  # downloads wordnet
nltk.download('averaged_perceptron_tagger')


lemmatizer = WordNetLemmatizer()
tokenizer = ToktokTokenizer()

stopword_list = nltk.corpus.stopwords.words('english')


def load_articles():
    articles = []
    try:
        with open("./articles/indianExp.json", encoding='utf-8') as f:
            data = json.load(f)
            articles += data
    except json.decoder.JSONDecodeError as e:
        data = []
    return articles


articles = load_articles()


def remove_punctuations(text):
    """Removes punctuation from text"""
    text = text.strip()
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r'[^\w\s]', '', text)
    return text


def decontact(phrase):
    """Removes apostrophe word and numbers"""
    # number
    phrase = re.sub(r'\b\d+\b', '', phrase)
    phrase = re.sub(r'\’', '\'', phrase)

    # specific
    phrase = re.sub(r"won't", "will not", phrase)
    phrase = re.sub(r"can\'t", "can not", phrase)

    # general
    phrase = re.sub(r"n\'t", " not", phrase)
    phrase = re.sub(r"\'re", " are", phrase)
    phrase = re.sub(r"\'s", " is", phrase)
    phrase = re.sub(r"\'d", " would", phrase)
    phrase = re.sub(r"\'ll", " will", phrase)
    phrase = re.sub(r"\'t", " not", phrase)
    phrase = re.sub(r"\'ve", " have", phrase)
    phrase = re.sub(r"\'m", " am", phrase)
    return phrase


def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)


def capture_lemmatization(tokens):
    """Captures lemmatization and translates word accordingly"""
    tokens = [lemmatizer.lemmatize(
        token, get_wordnet_pos(token)) for token in tokens]
    return tokens


def generate_tokens(text):
    """Generates tokens using tokenizer"""
    text = text.lower()
    tokens = tokenizer.tokenize(text)
    return tokens


def query_processing(query):

    vectorizer = pickle.load(open('./models/vectorizer.pickle', 'rb'))

    query_tokens = generate_tokens(query)
    query_tokens = capture_lemmatization(query_tokens)
    query_res = ' '.join(query_tokens)
    query_vec = vectorizer.transform([query_res])

    tfidf = pickle.load(open('./models/tfidf_matrix.pickle', 'rb'))

    sims = cosine_similarity(query_vec, tfidf)
    sims = [(i, sim) for i, sim in enumerate(sims[0])]
    sims = sorted(sims, key=lambda item: -item[1])

    return sims
