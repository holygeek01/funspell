import funspell

_text = "where is the ofice and the poduct"
#assuming  ngram.pkl file is present in "/home/data/" 
fun_spell  = FunSpell("/home/data/")

# updating the vocabulary using vocab.csv, vocab.csv is a single column csv file with list of new words which should be added to the dictionary
# header of csv column should be 'words'
#assuming vocabulary file present in /home/data/ path"

fun_spell.update_vocabulary_file("/home/data/vocab.csv")
print(funspell.correct(_text, 3))
