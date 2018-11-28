import flask
app = flask.Flask(__name__)
from nltk.tag import StanfordPOSTagger
import random


@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/submitted', methods=['POST', 'GET'])
def submitted():
    if flask.request.method == 'POST':             
        
        tagged_text = tag_text(flask.request.form['user_content'])
        rand_blanks = get_blanks(tagged_text)

        return flask.render_template('madlib_form.html', 
            user_content=rand_blanks)
        # return str(flask.request.form['user_content'].split('\n'))
    else:
        return 'this was a get'

def tag_text(text):
    ''' this function will take in the user text and run it through the stanford
        POS tagger and return a list of tagged words. 
    '''
    st = StanfordPOSTagger('english-left3words-distsim.tagger',
        path_to_jar='stanford-postagger-3.9.2.jar')
    # here we replace new lines with ' -: ' because otherwise the tagger will
    # get rid of the \n and we won't be able to reassemble the text of the user
    return st.tag(text.replace('\n', ' -: ').split(' '))


def get_blanks(tagged_text):
    ''' this function will take the tagged text and return a list of words that
        the users will pick the words for. '''

    # here is the basic list of part of speech that we want to give the user a 
    # as a blank in their madlib
    pos_tag_dict = {
        'JJ': 'Adjective',
        'RB': 'Adverb',
        'NN': 'Noun',
        'VB': 'Verb',
        'NP': 'Proper Noun',
    }

    # this while loop goes through and seperates the tagged text into list of lists
    # seperating it at the new lines or -:
    sentence_list = []
    index = 0
    while True:
        if index > len(tagged_text) - 1:
            sentence_list.append(tagged_text[0:index])
            break
        elif tagged_text[index][0].strip() == '-:':
            sentence_list.append(tagged_text[0:index])
            del tagged_text[0:index + 1]
            index = 0
        else:
            index += 1

    # this list comperhension will create a possible list of choices for each sentence
    # it does this by filtering away words with tags that don't match a key in the
    # pos_tag_dict.
    possible_choices = [
        # the slice here is because the stanford tagger tags speach in a more precise
        # way than what we want for the madlib so we only care about the first two 
        # characters in the string matching
        list(filter(lambda x: pos_tag_dict.get(x[1][:2]), sentence))
        for sentence in sentence_list
    ]

    # return list(map(random.choice, possible_choices))
    return [
        random.choice(options)
        for options in possible_choices
        if options
    ]
        


