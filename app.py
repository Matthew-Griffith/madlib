import flask
app = flask.Flask(__name__)
from nltk.tag import StanfordPOSTagger


@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/submitted', methods=['POST', 'GET'])
def submitted():
    if flask.request.method == 'POST':        
        
        st = StanfordPOSTagger('english-left3words-distsim.tagger',
            path_to_jar='stanford-postagger-3.9.2.jar')
        user_content = [
            st.tag(line.split(' ')) 
            for line in flask.request.form['user_content'].split('\n')
        ]       
        
        return flask.render_template('madlib_form.html', user_content=user_content)
        # return str(flask.request.form['user_content'].split('\n'))
    else:
        return 'this was a get'