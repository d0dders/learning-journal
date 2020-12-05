from flask_wtf import Form
from wtforms import StringField, DateField, TextAreaField, PasswordField
from wtforms.validators import (DataRequired, Regexp, Email, EqualTo, Length,
                                ValidationError)
from models import User


def name_exists(form, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError('User with that name already exists.')


def email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError('User with that email already exists.')


class EntryForm(Form):
    title = StringField(
        'Title',
        validators=[
            DataRequired()
        ]
    )
    created_date = DateField(
        'Date',
        validators=[
            DataRequired()
        ],
        render_kw={"type": "date"}
    )
    time_spent = StringField(
        'Time Spent',
        validators=[
            DataRequired()
        ]
    )
    learned = TextAreaField(
        'What I Learned',
        validators=[
            DataRequired()
        ]
    )
    resources = TextAreaField(
        'Resources to Remember',
        description="add each resource on a new line"
    )
    tags = StringField(
        "Tags",
        description="add '#' in front of each tag"
    )


class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class RegisterForm(Form):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-Z0-9_]+$',
                message=("Username should be one word, letters, "
                         "number, and underscores only")
            ),
            name_exists
        ]
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            email_exists
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=2),
            EqualTo('password2', message='Passwords must match')
        ]
    )
    password2 = PasswordField(
        'Confirm Password',
        validators=[DataRequired()]
    )