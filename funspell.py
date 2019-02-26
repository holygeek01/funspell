"""
Funspell is An automatic spell corrector using statistical n-gram models. This is a module which help us to build our custom n-gram model and make use of that language model to perform a context aware automatic spell correction.
"""
import pickle
import os
import re
from nltk.util import ngrams
import hunspell
import string
import collections


class Funspell():
    def __init__(self,file_path='./'):
        self.h = hunspell.HunSpell("/usr/share/hunspell/en_US.dic", "/usr/share/hunspell/en_US.aff")
        self.spell = self.h.spell
        self.file_path=file_path
        try:
            self.model = open(os.path.join(self.file_path, "ngram.pkl"), "rb")
            self.ngram_model = pickle.load(self.model)
            self.model.close()
        except Exception:
            print("please build n-gram first")
            exit()

    def build_ngram( self, data_file,file_path):
        """A method which estimate the n-grams and persist it to disk
        Keyword parameters:
        data_file:str
        file name which data is stored
        file_path:str
        file path the file exists
        A pkl file will be generated.
        """

        try:
            file=open(os.path.join(file_path, data_file), "rb")
            text=str(file.read())
            file.close()
        except e:
            print(e)
            exit()
        punctuationNoPeriod = "[" + re.sub("\.","",string.punctuation)+ "]"
        text = re.sub(punctuationNoPeriod, "", text)

        #getting the tokens
        tokenized=text.split()
        ngram_dict={}
        #getting ngrams
        esBigrams=ngrams(tokenized,2)
        esUnigrams=ngrams(tokenized,1)
        esTrigrams=ngrams(tokenized,3)
        es4grams=ngrams(tokenized,4)
        es5grams=ngrams(tokenized,5)
        #getting frequencies of each ngrams
        ngram_freq=dict()
        esBigramFreq=dict(collections.Counter(esBigrams))
        ngram_freq.update(esBigramFreq)
        esUnigramFreq=dict(collections.Counter(esUnigrams))
        ngram_freq.update(esUnigramFreq)
        esTrigramFreq=dict(collections.Counter(esTrigrams))
        ngram_freq.update(esTrigramFreq)
        es4gramFreq=dict(collections.Counter(es4grams))
        ngram_dict.update(es4gramFreq)
        es5gramFreq=dict(collections.Counter(es5grams))
        ngram_freq.update(es5gramFreq)

        ngram=open('ngram.pkl','wb')
        pickle.dump(ngram_freq,ngram)
        print("files saved")

    def update_vocabulary_file(self, file_path="./"):
        """update HunSpell vocabulary using csv
        keyword argument:
        -------
        file_path:str
        a csv file name in the root directory
        """
        import pandas as pd

        hunspell_add = self.h.add
        try:
            file_name = "vocab.csv"
            df = pd.read_csv(os.path.join(file_path, file_name))
            words_to_add = list(df.words)

        except Exception as e:
            print(e)
            return

        words_to_add = map(str.lower, words_to_add)
        for each_taken in words_to_add:
            hunspell_add(each_taken)


    def get_relevant_suggestions(self, words):
        """a function to reduce the number of suggestions using unigrams    
        keyword parameters:
        words:list
        list of suggested words by hunspell 
        return values:
        relevant_suggestions:list
        list of words present in unigram model
        """
        relevant_suggestions = list()
        relevant_suggestions_append = relevant_suggestions.append
        for each_words in ngrams(words, 1):
            try:
                rel_freq = self.ngram_model[each_words]
                if rel_freq > 0:
                    for each in each_words:
                        relevant_suggestions_append(each)
            except KeyError:
                pass
        return relevant_suggestions


    def get_wrong_words(self, query):
        """find mispelled words and returns the list.
        if their is no mispelled words, exit the module
        keyword argument:
        query:str
        the input query as a string 
        return values:
        wrong_words:list
        list of mispelled words found in input text 
        """
        query = re.sub(r"[^\w\s]", "", query)
        query_tokens = query.lower().split()
        wrong_words = list()
        wrong_append = wrong_words.append

        for each in query_tokens:
            if not self.spell(each):
                wrong_append(each)
        if len(wrong_words) == 0:
            print("no corrections")
            exit()
        else:
            return wrong_words


    def get_relevant_ngrams(self, tokenized_sentences, suggested_words, ngram_type):
        """A method to create ngram for given 'n' and filter the relevant ngrams
        keyword arguments:
        tokenized_sentences:list(list)
        list of tokenized sentences
        suggested_words:list
        list of hunspell suggestions for the wrong words 
        ngram_type:int
        value of 'N' to choose the ngram
        return values:
        suggested_gram_dict:dict
        a dictionary with ngrams of each suggested words
        """

        all_ngrams = list()
        all_ngrams_append = all_ngrams.append
        for tok in tokenized_sentences:
            all_ngrams_append(list(ngrams(tok, ngram_type)))
        grams_ = list()
        grams_append = grams_.append
        for each in all_ngrams:
            for each_gram in each:
                grams_append(each_gram)

        suggested_gram_dict = dict()
        for h_suggest in suggested_words:
            suggested_gram_dict[h_suggest] = []
            for each_bigram in grams_:
                if h_suggest in each_bigram:
                    suggested_gram_dict[h_suggest].append(each_bigram)

        return suggested_gram_dict


    def correct_spelling(self, incorrect_word, input_text, value_of_n):
        """this function will find the correct word for the wrong word given and insert it into the query
        parameters
        -------
        incorrect_word:str
        incorrect word in the sentence 
        query:str
        the sentence given by the user 
        value_of_n:int
        value of n to check,2gram through 5gram(default is 2)
        returns
        -------
        ultimate_result:str
        returns the corrected sentence 
        """
        try:
            suggested_words = self.h.suggest(incorrect_word)
            if len(suggested_words)<1:
                print("Sorry, No spelling suggestion found,  try updating the Hunspell dictionary")
                exit()
            suggested_words = self.get_relevant_suggestions(suggested_words)
        except:
            pass
        if len(suggested_words) == 1:
            result = suggested_words[0]
            ultimate_result = input_text.replace(incorrect_word, result)
            return ultimate_result

        elif len(suggested_words) > 1:
            sentence_list = list()
            sentence_list_append = sentence_list.append
            replace = input_text.replace
            for word in suggested_words:
                sentence_list_append(replace(incorrect_word, word))
            # print(sentence_list)
            tokens_list = list(map(str.split, sentence_list))
            print(tokens_list)
            exit()
        gram_dict = self.get_relevant_ngrams(tokens_list, suggested_words, value_of_n)
        # print(gram_dict)
        frequency_list = [0] * 20
        for ind, each_hspell in enumerate(suggested_words, 0):
            for _2gram in gram_dict[each_hspell]:
                try:
                    frequency_list[ind] += self.ngram_model[_2gram]
                except KeyError:
                    pass

        result_index = frequency_list.index(max(frequency_list))
        result = suggested_words[result_index]
        ultimate_result = input_text.replace(incorrect_word, result)
        return ultimate_result


    def correct(self, _text, value_of_n=2):
        """A function to get input and perform spell correction after checking conditions
        keyword parameters:
        _text:str
        input text to the module which should be corrected(should not be empty)
        value_of_n:int
        value of 'n' of ngram(default is 2)
        """

        if len(_text) == 0:
            raise ValueError("given text is empty")

        elif value_of_n < 2 or value_of_n > 5:
            raise ValueError("Allowed value of 'n' are 2,3,4,5")

        after_correction = _text
        wrong = self.get_wrong_words(_text)
        

        if len(wrong)<1:
            print("no wrong words found")
            exit()
        for each_wrong in wrong:
            after_correction = self.correct_spelling(
                each_wrong, after_correction, int(value_of_n)
            )
        return after_correction

if __name__=="__main__":
    from funspell import Funspell
    f=Funspell()
    #f.update_vocabulary_file() #CSV should be present in the current folder(./)
    inp=input("enter the text \n")
    print(f.correct(inp))