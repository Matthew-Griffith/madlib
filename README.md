# madlib
this is for a website that will take in a block of text and let you turn it into a mablib for you

it does this by first using standford's POS tagger, which can be downloaded [here](https://nlp.stanford.edu/software/tagger.shtml#Download)
after the text is tagged it randomly choose word for the user to replace and serves them a new form.
then it will replace the word in the original text and return that to the user.

this project makes use a flask and nltk(this is to simplify using the standford POS tagger).
in order to run this project locally you would need to pip install flask and nltk. and you need to place the
standford pos tagger jar and model file in the same directory as app.py
