import flask
app = flask.Flask(__name__)


@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/submitted', methods=['POST', 'GET'])
def submitted():
    if flask.request.method == 'POST':
        user_content = flask.request.form['user_content']
        return flask.render_template('madlib_form.html', user_content=user_content)
        # return str(flask.request.form['user-content'])
    else:
        return 'this was a get'