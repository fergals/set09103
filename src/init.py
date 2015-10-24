from flask import Flask, render_template
from movies import Content

TOPIC_DICT = Content()

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template("main.html")
	
@app.route ('/movies/')
@app.route ('/movies/<name>/')
def hello ( name = None ):
	return render_template ('categories.html', name=name, TOPIC_DICT = TOPIC_DICT)

@app.errorhandler(404)
def page_not_found(error):
	return render_template("404.html")
	
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)