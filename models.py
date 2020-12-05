import datetime
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash
from peewee import *


DATABASE = SqliteDatabase('journal.db')


class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    is_admin = BooleanField(default=False)

    class Meta:
        database = DATABASE

    @classmethod
    def create_user(cls, username, email, password, admin=True):
        try:
            with DATABASE.transaction():
                cls.create(
                    username=username,
                    email=email,
                    password=generate_password_hash(password),
                    is_admin=admin
                )
        except IntegrityError:
            raise ValueError("User already exists")


class Entry(Model):
    created_date = DateTimeField(default=datetime.datetime.now)
    title = CharField()
    time_spent = CharField()
    learned = TextField()
    resources = TextField()
    user = ForeignKeyField(User, backref='entries')

    class Meta:
        database = DATABASE

    def get_author_name(self):
        return User.get_by_id(self.user).username


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
    DATABASE.create_tables([Entry, Tag, User], safe=True)
    DATABASE.close()
