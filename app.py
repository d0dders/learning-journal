import models
import forms
from flask import Flask, g, render_template, redirect, url_for, abort


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
        entry_id = models.Entry.create(
            title=form.title.data.strip(),
            created_date=form.created_date.data,
            time_spent=form.time_spent.data.strip(),
            learned=form.learned.data.strip(),
            resources=form.resources.data.strip()
        ).get_id()
        for tag in form.tags.data.strip().split('#')[1:]:
            models.Tag.create(
                entry=entry_id,
                tag_name=tag.strip()
            )
        return redirect(url_for('index'))
    return render_template('new.html', form=form)


@app.route('/entries/<int:entry_id>/delete')
def delete(entry_id):
    try:
        models.Entry.get_by_id(entry_id).delete_instance()
        models.Tag.delete().where(models.Tag.entry == entry_id).execute()
    except models.DoesNotExist:
        abort(404)
    else:
        return redirect(url_for('index'))


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
        models.Tag.delete().where(models.Tag.entry == entry_id).execute()
        for tag in form.tags.data.strip().split('#')[1:]:
            models.Tag.create(
                entry=entry_id,
                tag_name=tag.strip()
            )
        return redirect(url_for('index'))
    try:
        entry = models.Entry.get_by_id(entry_id)
        tag_string = ''
        for tag in entry.tags:
            tag_string += '#'+tag.tag_name+' '
        entry.tags = tag_string.strip()
        form = forms.EntryForm(obj=entry)
    except models.DoesNotExist:
        abort(404)
    else:
        return render_template('edit.html', form=form, entry=entry)


@app.route('/entries/<int:entry_id>')
def detail(entry_id):
    try:
        entry = models.Entry.get_by_id(entry_id)
    except models.DoesNotExist:
        abort(404)
    else:
        return render_template('detail.html', entry=entry)


@app.route('/')
@app.route('/entries')
def index():
    entries = models.Entry.select().limit(100).order_by(
        models.Entry.created_date.desc())
    return render_template('index.html', entries=entries)


@app.errorhandler(404)
def not_found(error):
    return '404', 404


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
        try:
            models.Tag.create(
                entry=1,
                tag_name="Python"
            )
            models.Tag.create(
                entry=1,
                tag_name="Flask"
            )
            models.Tag.create(
                entry=1,
                tag_name="Learning"
            )
        except models.IntegrityError:
            pass
    app.run(debug=DEBUG, host=HOST, port=PORT)
