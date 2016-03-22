from flask_restful import fields

question_option = {
    'id': fields.String,
    'name': fields.String
}

survey_question = {
    'id': fields.String,
    'name': fields.String,
    'description': fields.String,
    'type': fields.String,
    'options': fields.List(fields.Nested(question_option))
}

survey_fields = {
    'id': fields.String,
    'name': fields.String,
    'description': fields.String,
    'questions': fields.List(fields.Nested(survey_question))
}