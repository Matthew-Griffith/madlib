import flask
app = flask.Flask(__name__)
from nltk.tag import StanfordPOSTagger
import random
import re


@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/submitted', methods=['POST', 'GET'])
def submitted():
    if flask.request.method == 'POST':        

        # here will get the tagged text from the form the user filled out on the
        # index page of the site
        tagged_text = tag_text(flask.request.form['user_content'])
        # here we take our tagged text and find random blanks for certain POS
        rand_blanks = get_blanks(tagged_text)

        return flask.render_template('madlib_form.html', 
            blank_words=rand_blanks,
            original_text=flask.request.form['user_content'].replace('\n', '_'))

    else:
        return 'this was a get'

@app.route('/your_madlib/<string:original_text>', methods=['POST'])
def your_madlib(original_text):
    
    # here we turn the original text into a list of lists. where the inner lists
    # containing the word for each line.
    madlib_list = map(lambda sentence: sentence.split(' '), original_text.split('_'))
    # here we just won't the make the original words list lower case for matching
    # them in the nest for loop below
    original_words = list(map(lambda word: word.lower(), flask.request.form))

    # here we are going to loop over the whole madlib_lists to check if each word should
    # be replaced, if it should we replacing by add the user selected word to the madlib
    # string that we will return the user.
    finished_madlib = []
    for sentence in madlib_list:
        madlib_line=''
        for word in sentence:
            if word.lower() in original_words:
                madlib_line += ' ' + flask.request.form[word]
            else:
                madlib_line += ' ' + word
        finished_madlib.append(madlib_line.lstrip())
    
    return flask.render_template('user_madlib.html', madlib=finished_madlib)

def tag_text(text):
    ''' 
        this function will take in the user text and run it through the stanford
        POS tagger and return a list of tagged words. 
    '''
    st = StanfordPOSTagger('english-left3words-distsim.tagger',
        path_to_jar='stanford-postagger-3.9.2.jar')
    # here we replace new lines with ' -: ' because otherwise the tagger will
    # get rid of the \n and we won't be able to reassemble the text of the user
    return st.tag(text.replace('\n', ' -: ').split(' '))


def get_blanks(tagged_text):
    ''' 
        this function will take the tagged text and return a list of words that
        the users will pick the words for.
    '''
    # TODO: this function seems too long, maybe break it into smaller functions?

    # here is the basic list of part of speech that we want to give the user a 
    # as a blank in their madlib
    pos_tag_dict = {
        'JJ': 'Adjective',
        # 'RB': 'Adverb',
        'NN': 'Noun',
        'VB': 'Verb',
        'NNP': 'Proper Noun',
    }

    # this while loop goes through and seperates the tagged text into list of lists
    # seperating it at the new lines or -:
    sentence_list = []
    index = 0
    while True:
        if index > len(tagged_text) - 1:
            sentence_list.append(tagged_text[:index])
            break
        elif tagged_text[index][0].strip() == '-:':
            sentence_list.append(tagged_text[:index])
            del tagged_text[0:index + 1]
            index = 0
        else:
            index += 1

    # this list comperhension will create a possible list of choices for each sentence
    # it does this by filtering away words with tags that don't match a key in the
    # pos_tag_dict. 
    # https://repository.upenn.edu/cgi/viewcontent.cgi?article=1603&context=cis_reports
    possible_choices = [
        # the slice here is because the stanford tagger tags speach in a more precise
        # than what we want for the madlib so we only care about the first two 
        # characters in the string matching
        list(filter(lambda tagged_word: pos_tag_dict.get(tagged_word[1][:2]), sentence))
        for sentence in sentence_list
    ]

    # here we create a set of words up to 10 and then return it.
    blank_words = set()
    for words in possible_choices:
        if not words or len(blank_words) > 9:
            pass
        else:
            # here we get a random word and then remove the punctation(regex) from 
            # the word and give the part of speach a more readable name for later
            rand_word = random.choice(words)
            user_word = re.sub('[.!?]', '', rand_word[0])
            if rand_word[1][:3] == 'NNP':
                pos = 'Proper Noun'
            else:
                pos = pos_tag_dict.get(rand_word[1][:2])

            blank_words.add((user_word, pos))
    return blank_words

        


