import datetime
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash
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


class User(UserMixin, Model):
    username = CharField(unique=True)
    password = CharField(max_length=100)
    is_admin = BooleanField(default=False)

    class Meta:
        database = DATABASE

    @classmethod
    def create_user(cls, username, password, admin=True):
        try:
            with DATABASE.transaction():
                cls.create(
                    username=username,
                    password=generate_password_hash(password),
                    is_admin=admin
                )
        except IntegrityError:
            raise ValueError("User already exists")


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Entry, Tag, User], safe=True)
    DATABASE.close()
