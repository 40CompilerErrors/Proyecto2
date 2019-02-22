import string

from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize


class Text_Processing:
    """
    All NLP process is done here
    """

    def __init__(self):
        """
        Class constructor
        """
        self.__reviews = []

    def tokenizer(self, reviews):
        """
        Tokenizing, stemming and stop words filtering process
        :param reviews:
        :return : list
        """
        stems = []
        stop_words = set(stopwords.words('spanish'))
        token = word_tokenize(text=reviews, language='spanish')
        for item in token:
            if item not in stop_words and item not in string.punctuation:
                stems.append(SnowballStemmer(language='spanish').stem(item))

        self.__reviews = stems
        return stems

    def graph_reviews(self):
        """
        Dani didn't want this graph, but it may be useful (or not), returns a frequency word distribution graph
        :return: plot
        """
        fdist = FreqDist(self.__reviews)
        print(fdist)
        fdist.plot(30, cumulative=False)
        return fdist
