from flask.ext.mongoengine import MongoEngine

db = MongoEngine()


class User(db.Document):
    sub = db.StringField(required=True, primary_key=True)
    email = db.StringField(required=True)
    admin = db.BooleanField(required=True, default=False)
    first_name = db.StringField(required=True)
    last_name = db.StringField(required=True)


class QuestionOption(db.EmbeddedDocument):
    id = db.StringField(required=True)
    name = db.StringField(required=True)


class Question(db.EmbeddedDocument):
    id = db.StringField(required=True)
    name = db.StringField(required=True)
    description = db.StringField()
    type = db.StringField(required=True, choices=['text', 'paragraph', 'radio', 'checkbox', 'select'])
    options = db.EmbeddedDocumentListField(QuestionOption)


class Survey(db.Document):
    author = db.ReferenceField(User, required=True)
    name = db.StringField(required=True)
    description = db.StringField()
    questions = db.EmbeddedDocumentListField(Question)


class AnswerItem(db.EmbeddedDocument):
    question = db.StringField(required=True)
    answer = db.StringField()


class Answer(db.Document):
    survey = db.ReferenceField(Survey, required=True)
    answers = db.EmbeddedDocumentListField(AnswerItem)