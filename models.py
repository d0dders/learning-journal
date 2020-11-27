import datetime
from peewee import *


DATABASE = SqliteDatabase('journal.db')


class Entry(Model):
    created_date = DateTimeField(default=datetime.datetime.now)
    content = TextField()
    time_spent = CharField(max_length=30)
    learned = TextField()
    resources = TextField()

    class Meta:
        database = DATABASE


class Tag(Model):
    entry = ForeignKeyField(Entry, backref="tags")
    tag_name = CharField(max_length=50)

    class Meta:
        database = DATABASE
        indexes = (
            (('entry', 'tag_name'), True), 
        )


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Entry, Tag], safe=True)
    DATABASE.close()