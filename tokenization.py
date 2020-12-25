import re
import spacy
from langdetect import detect
from string import punctuation
from nltk.corpus import stopwords as sw

def tokenization_process(text : str) -> list: #tokenization of text words using spacy and other techniques



    if re.sub(re.compile('\d|\:|\s|\-|\+|\!|\/|\,|\.|\=|\?|\！|\砰'), '', text) != '':

        #STOPWORDS
        lang = ['arabic', 'azerbaijani', 'danish', 'dutch', 'english', 'finnish', 'french', 'german', 'greek',
                'hungarian',
                'indonesian', 'italian', 'kazakh', 'nepali', 'norwegian', 'portuguese', 'romanian', 'russian',
                'slovene',
                'spanish', 'swedish', 'tajik', 'turkish']

        try:
            stopwords = set(sw.words('english'))
        except:
            stopwords = set()

        for l in lang:
            try:
                stopwords = stopwords.union(set(sw.words(l)))
            except:
                stopwords = stopwords





        try:
            language = detect(text)
        except:
            language = 'en'


        if(language == 'en'):
            nlp = spacy.load("en_core_web_sm")
        elif (language == 'zh'):
            nlp = spacy.load("zh_core_web_sm")
        elif (language == 'da'):
            nlp = spacy.load("da_core_news_sm")
        elif (language == 'nl'):
            nlp = spacy.load("nl_core_news_sm")
        elif (language == 'fr'):
            nlp = spacy.load("fr_core_news_sm")
        elif (language == 'de'):
            nlp = spacy.load("de_core_news_sm")
        elif (language == 'el'):
            nlp = spacy.load("el_core_news_sm")
        elif (language == 'it'):
            nlp = spacy.load("it_core_news_sm")
        elif (language == 'ja'):
            nlp = spacy.load("ja_core_news_sm")
        elif (language == 'lt'):
            nlp = spacy.load("lt_core_news_sm")
        elif (language == 'nb'):
            nlp = spacy.load("nb_core_news_sm")
        elif (language == 'pl'):
            nlp = spacy.load("pl_core_news_sm")
        elif (language == 'pt'):
            nlp = spacy.load("pt_core_news_sm")
        elif (language == 'ro'):
            nlp = spacy.load("ro_core_news_sm")
        elif (language == 'es'):
            nlp = spacy.load("es_core_news_sm")
        else:
            # print('inter')
            nlp = spacy.load("xx_ent_wiki_sm")

        tokens = [x.lemma_.lower() for x in nlp(text) if (x.pos_ not in ['PUNCT', 'SPACE']) and (not x.is_stop)]

        trash_tokens = ['–', '-', 'le', 'de', 'del', 'dell', 'della', 'l', 'degli', "dell'", "l'", '’', 'l’', 'dell’',
                        '.', '?', '!', '¡', 'a', 'do', '(', ')', 'e-', 'e', 'el', 'r', 'n', 'se', 'una', 'alla', 'la',
                        "'", 'to', 'of', 'o', "'n", 'y', "'s", ',', "'t", 'don', 'the', '・', 'u', '」', '「', 'в',
                        'por', 'el', 'du', 'les', '']


        tokens = [x for x in tokens if (x not in punctuation) and (x not in stopwords) and (x not in trash_tokens)]

        return tokens

    else:
        return [text]