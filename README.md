# **funspell**


**Funspell** is An automatic spell corrector using statistical n-gram models. This is a module which help us to build our custom n-gram model and make use of that language model to perform a context aware automatic spell corrector. The spell corrector is build on top of the famous spell checker library [hunspell](https://github.com/hunspell/hunspell Hunspell home page"") which is used by most popular free softwares such as Mozilla Firefox, Google Chrome etc. **Funspell**can be used in chat bots and other conversational interfaces to correct the input queries and other medium sized documents to perform automatic spell correction with the use of custom built n-gram model with data in our hand. 


## Prerequisites 


Since hunspell is a unix based software, this module will work only on linux and Mac platform currently. We need to install the following packages using our package manager. This are the instructions for linux platform and Mac users can map this commands with their own package management tools. 


- sudo apt-get install python-dev: Needed python dev tools 

-  sudo apt-get install libhunspell-dev : Installing Hunspell native library files 

- PIP install nltk, pandas # essential packages 

- pip install hunspell : Installing the hunspell python wrapper to be used by **funspell**


## How to use it

refer the demo.py to understand how to perform spell correction.

- A n-gram model has to be build to use the spell corrector.
-  We can use any online available corpus like wikipedia or custom corpus to build n-gram model. 

To build n-gram model:

run "python3 funspell.py [path todata/corpus] ['file name.txt] [output path to save the model]

Use the "ngram.pkl" file generated from the above step to instantiate.

We can add custom words to avoid unwanted correction using "update_vocabulary_file()" function in Funspell class.


## Root of the Idea

The idea for this spell corrector is inspired by the paper 'spelling correction using N-grams'by David Sundby. You can check it from the reference folder. 

