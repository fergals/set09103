from flask import Flask, render_template, g
import sqlite3

DATABASE = 'movieinfo.db'

app = Flask(__name__)
app.config.from_object(__name__) ##connect to config file

def connect_db():
	return sqlite3.connect(app.config['DATABASE']) ##connect to database

@app.route('/')
def homepage():
	g.db = connect_db()
	cur = g.db.execute('select movie_name, director, year, gross, poster, category, studio from movies') 
	movies = [dict(movie_name=row[0], director=row[1], year=row[2], gross=row[3], poster=row[4], category=row[5], studio=row[6])  for row in cur.fetchall()] #adds database data to dictionary
	g.db.close()
	return render_template('main.html', movies=movies)
	
@app.route ('/movies/')
@app.route ('/movies/<name>/')
def movies ( name = None ):
	return render_template ('categories.html', name=name)
	
@app.route ('/movies/genre/<name>/')
def genre ( name = None ):
	return render_template ('genre.html', name=name)
	
@app.errorhandler(404)
def page_not_found(error):
	return render_template("404.html")
	
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)