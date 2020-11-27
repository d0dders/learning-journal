import models
import forms
from flask import Flask, g, render_template, redirect, url_for


DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = 'lakfbalgnef28r2u$$£^%"ffsseffe!£!!$"£fefeawu&&"'


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


@app.route('/new', methods=('GET', 'POST'))
def new():
    form = forms.EntryForm()
    if form.validate_on_submit():
        models.Entry.create(
            title=form.title.data.strip(),
            created_date=form.created_date.data,
            time_spent=form.time_spent.data.strip(),
            learned=form.learned.data.strip(),
            resources=form.resources.data.strip()
        )
        return redirect(url_for('index'))
    return render_template('new.html', form=form)


@app.route('/entries/<int:entry_id>/edit', methods=('GET', 'POST'))
def edit(entry_id):
    form = forms.EntryForm()
    if form.validate_on_submit():
        models.Entry.update(
            title=form.title.data.strip(),
            created_date=form.created_date.data,
            time_spent=form.time_spent.data.strip(),
            learned=form.learned.data.strip(),
            resources=form.resources.data.strip()
        ).where(models.Entry.id == entry_id).execute()
        return redirect(url_for('index'))
    entry = models.Entry.get_by_id(entry_id)
    form = forms.EntryForm(obj=entry)
    return render_template('edit.html', form=form, entry=entry)


@app.route('/entries/<int:entry_id>')
def detail(entry_id):
    entry = models.Entry.get_by_id(entry_id)
    return render_template('detail.html', entry=entry)


@app.route('/')
@app.route('/entries')
def index():
    entries = models.Entry.select().limit(100).order_by(
        models.Entry.created_date.desc())
    return render_template('index.html', entries=entries)


if __name__ == "__main__":
    models.initialize()
    if models.Entry.select().count() == 0:
        try:
            models.Entry.create(
                title="This is my first journal entry.",
                time_spent="3 Days",
                learned="How to build a learning journal using Python",
                resources="Team Treehouse"
                )
        except ValueError:
            pass
    app.run(debug=DEBUG, host=HOST, port=PORT)
