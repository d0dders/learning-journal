from flask_wtf import Form
from wtforms import StringField, DateField, TextAreaField
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
        validators=[DataRequired()]
    )