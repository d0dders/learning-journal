from flask_wtf import Form
from wtforms import StringField, DateField, TextAreaField, PasswordField
from wtforms.validators import DataRequired


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
        ]
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
