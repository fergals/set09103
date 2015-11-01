from flask import Flask, render_template, g 
import sqlite3

app = Flask(__name__)

@app.route('/')
def homepage(name=None):
    g.db = connect_db()
    cur = g.db.execute('select id, movie_name, poster from movies order by random() limit 14')  #selects data from database
    movies = [dict(id=row[0], movie_name=row[1], poster=row[2]) for row in cur.fetchall()] # adds data to dictionary
    g.db.close()
    return render_template('main.html', movies=movies, name=name)

@app.route('/movies/<id>/')
def movie(id=None):
    g.db = connect_db()
    cur = g.db.execute('select id, movie_name, director, year, gross, poster, category, studio, rating, synopsis from movies where id = ?', [id])
    movies = [dict(id=row[0], movie_name=row[1], director=row[2], year=row[3], gross=row[4], poster=row[5], category=row[6], studio=row[7], rating=row[8], synopsis=row[9]) for row in cur.fetchall()]
    g.db.close()
    return render_template('individualmovie.html', movies=movies, id=id)

@app.route('/movies/genres/<name>/')
def genres(name=None):
    g.db = connect_db()
    cur = g.db.execute('select id, movie_name, poster from movies where category = ?', [name])
    movies = [dict(id=row[0], movie_name=row[1], poster=row[2]) for row in cur.fetchall()]
    g.db.close()
    return render_template('genres.html', movies=movies, name=name)
	
@app.route('/movies/upcoming/')
def upcoming(name='Upcoming'):
    g.db = connect_db()
    cur = g.db.execute('select id, movie_name, poster from movies where year = "2016"')
    movies = [dict(id=row[0], movie_name=row[1], poster=row[2]) for row in cur.fetchall()]
    g.db.close()
    return render_template('upcoming.html', movies=movies, name=name)
	
@app.route('/movies/top-rated/')
def toprated(name='Top Rated'):
    g.db = connect_db()
    cur = g.db.execute('select id, movie_name, poster, rating from movies where rating = 5')
    movies = [dict(id=row[0], movie_name=row[1], poster=row[2], rating=row[3]) for row in cur.fetchall()]
    g.db.close()
    return render_template('toprated.html', movies=movies, name=name)

def connect_db():
    return sqlite3.connect('movieinfo.db')

def init_db():
    conn = connect_db()
    c = conn.cursor()
    conn.commit()
    conn.close()

@app.errorhandler(404)
def page_not_found(error):
	return render_template("404.html"), 404
	
@app.errorhandler(400)
def page_not_found(error):
	return render_template("othererror.html"), 400
	
@app.errorhandler(401)
def page_not_found(error):
	return render_template("othererror.html"), 401
	
@app.errorhandler(500)
def page_not_found(error):
	return render_template("othererror.html"), 500

def main():
    init_db()
    app.run(host='0.0.0.0', debug=True)

if __name__ == '__main__':
    main()