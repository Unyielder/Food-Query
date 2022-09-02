from mongoengine import Document, StringField


class User(Document):
    id_token = StringField(required=True)
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    profile_url = StringField()

