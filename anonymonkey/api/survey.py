from flask import request
from flask_restful import Resource, reqparse, marshal_with, abort
from flask_login import current_user
from .fields import survey_fields
from anonymonkey.schemas import Survey, Question, QuestionOption, User


class SurveyListResource(Resource):
    @marshal_with(survey_fields)
    def get(self):
        surveys = Survey.objects
        if not current_user.is_admin():
            if 'author' not in request.args:
                return abort(401)
            if request.args['author'] != current_user.get_id():
                return abort(401)

        if 'author' in request.args:
            surveys = surveys.filter(author=User.objects.with_id(request.args['author']))

        return list(surveys.all())

    @marshal_with(survey_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=unicode, required=True)
        parser.add_argument('description', type=unicode)
        parser.add_argument('questions', type=list, location='json')
        args = parser.parse_args()

        questions = []
        for question in args['questions']:
            options = []
            for option in question['options']:
                options.append(QuestionOption(
                    id=option['id'],
                    name=option['name']
                ))
            questions.append(Question(
                id=question['id'],
                name=question['name'],
                description=question['description'],
                type=question['type'],
                options=options
            ))

        survey = Survey(
            name=args['name'],
            description=args['description'],
            questions=questions,
            author=current_user.user
        )

        survey.save()
        return survey


class SurveyResource(Resource):
    @marshal_with(survey_fields)
    def get(self, survey_id):
        survey = Survey.objects.with_id(survey_id)
        return survey