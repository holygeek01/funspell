import funspell

# _text=input("enter the query\n")
_text = "where is the ofice and the poduct"
"""
updating the vocabulary using vocab.csv, vocab.csv is a single column csv file with list of new words which should be added to the dictionary
"""
# header of csv column should be 'words'
single_bigram.update_vocabulary_file('vocab.csv')
print(funspell.correct(_text, 3))
