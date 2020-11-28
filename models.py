import datetime
from peewee import *


DATABASE = SqliteDatabase('journal.db')


class Entry(Model):
    created_date = DateTimeField(default=datetime.datetime.now)
    title = CharField()
    time_spent = CharField()
    learned = TextField()
    resources = TextField()

    class Meta:
        database = DATABASE


class Tag(Model):
    entry = ForeignKeyField(Entry, backref="tags")
    tag_name = CharField()

    class Meta:
        database = DATABASE
        indexes = (
            (('entry', 'tag_name'), True),
        )


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Entry, Tag], safe=True)
    DATABASE.close()
