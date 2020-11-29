import models
import forms
from flask import Flask, g, render_template, redirect, url_for, abort, flash
from flask_bcrypt import check_password_hash
from flask_login import (LoginManager, login_user, logout_user,
                         login_required, current_user)


DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = 'lakfbalgnef28r2u$$£^%"ffsseffe!£!!$"£fefeawu&&"'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connect to the db before each request"""
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    """Close the db connection after each request"""
    g.db.close()
    return response


@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.username == form.username.data)
        except models.DoesNotExist:
            flash("Your email or password doesn't match", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash("Your email or password doesn't match", "error")
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/new', methods=('GET', 'POST'))
@login_required
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
            try:
                models.Tag.create(
                    entry=entry_id,
                    tag_name=tag.strip()
                )
            except models.IntegrityError:
                pass
        return redirect(url_for('index'))
    return render_template('new.html', form=form)


@app.route('/entries/<int:entry_id>/delete')
@login_required
def delete(entry_id):
    try:
        models.Entry.get_by_id(entry_id).delete_instance()
        models.Tag.delete().where(models.Tag.entry == entry_id).execute()
    except models.DoesNotExist:
        abort(404)
    else:
        return redirect(url_for('index'))


@app.route('/entries/<int:entry_id>/edit', methods=('GET', 'POST'))
@login_required
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
            try:
                models.Tag.create(
                    entry=entry_id,
                    tag_name=tag.strip()
                )
            except models.IntegrityError:
                pass
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
@app.route('/<tag_name>')
def index(tag_name=None):
    if tag_name:
        matching_tags = models.Tag.select().where(
            models.Tag.tag_name ** tag_name)
        if len(matching_tags) == 0:
            abort(404)
        matching_entry_ids = [tag.entry_id for tag in matching_tags]
        try:
            entries = models.Entry.select().where(
                models.Entry.id << matching_entry_ids).limit(100).order_by(
                models.Entry.created_date.desc())
        except models.DoesNotExist:
            abort(404)
    else:
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
        models.User.create_user(
            username='admin',
            password='password',
            admin=True
            )
    except ValueError:
        pass
    app.run(debug=DEBUG, host=HOST, port=PORT)
