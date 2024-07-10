from mongoengine import Document, StringField, ListField


class UserInfo(Document):
    email = StringField(unique=True, required=True)
    verbs = ListField(StringField(max_length=100), default=list)
    nouns = ListField(StringField(max_length=100), default=list)
