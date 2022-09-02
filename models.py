from mongoengine import Document, StringField, IntField


class User(Document):
    id_token = StringField(required=True, unique=True)
    email = StringField(required=True, unique=True)
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    profile_url = StringField()


class Bookmark(Document):
    id_token = StringField(required=True, unique=True)
    food_code = IntField(required=True)
    food_desc = StringField(required=True)
    serving_size = StringField(required=True)

