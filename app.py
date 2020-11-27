import models
from flask import Flask, g, render_template, url_for

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)


@app.before_request
def before_request():
    """Connect to the db before each request"""
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    """Close the db connection after each request"""
    g.db.close()
    return response


@app.route('/new')
def new():
    return render_template('new.html')


@app.route('/entries/<int:entry_id>')
def detail(entry_id):
    entry = models.Entry.get_by_id(entry_id)
    return render_template('detail.html', entry=entry)


@app.route('/')
@app.route('/entries')
def index():
    entries = models.Entry.select().limit(100)
    return  render_template('index.html', entries=entries)



if __name__ == "__main__":
    models.initialize()
    if models.Entry.select().count() == 0:
        try:
            models.Entry.create(
                content = "This is my first journal entry.",
                time_spent = "3 Days",
                learned = "How to build a learning journal using Python and Flask",
                resources = 
                    """Team Treehouse
https://pythonbasics.org/flask-tutorial-templates/
http://docs.peewee-orm.com/projects/flask-peewee/en/latest/getting-started.html?highlight=response"""
                )
        except ValueError:
            pass
    app.run(debug=DEBUG, host=HOST, port=PORT)