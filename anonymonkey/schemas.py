from flask.ext.mongoengine import MongoEngine

db = MongoEngine()


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
    name = db.StringField(required=True)
    description = db.StringField()
    questions = db.EmbeddedDocumentListField(Question)
