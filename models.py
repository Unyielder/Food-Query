from mongoengine import Document, StringField


class User(Document):
    id_token = StringField(required=True, unique=True)
    email = StringField(required=True, unique=True)
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    profile_url = StringField()

