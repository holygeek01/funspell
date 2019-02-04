# **funspell**


**Funspell** is An automatic spell corrector using statistical n-gram models. This is a module which help us to build our custom n-gram model and make use of that language model to perform a context aware automatic spell corrector. The spell corrector is build on top of the famous spell checker library [hunspell](https://github.com/hunspell/hunspell Hunspell home page"") which is used by most popular free softwares such as Mozilla Firefox, Google Chrome etc. **Funspell**can be used in chat bots and other conversational interfaces to correct the input queries and other medium sized documents to perform automatic spell correction with the use of custom built n-gram model with data in our hand. 


## Prerequisites 


Since hunspell is a unix based software, this module will work only on linux and Mac platform currently. We need to install the following packages using our package manager. This are the instructions for linux platform and Mac users can map this commands with their own package management tools. 


*sudo apt-get install python-dev: Needed python dev tools 
*sudo apt-get install libhunspell: Installing Hunspell native library files 
*pip install hunspell : Installing the hunspell python wrapper to be used by **funspell**


## Example 

refer the test.py to understand how to perform spell correction.