from flask_restful import fields

user_fields = {
    'sub': fields.String,
    'email': fields.String,
    'admin': fields.Boolean,
    'first_name': fields.String,
    'last_name': fields.String
}

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