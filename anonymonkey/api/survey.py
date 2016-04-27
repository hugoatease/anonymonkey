from flask import request, current_app, render_template, url_for, jsonify
from flask_restful import Resource, reqparse, marshal_with, abort, marshal
from flask_login import current_user, login_required
from .fields import survey_fields
from anonymonkey.schemas import Survey, Question, QuestionOption, User, Answer
import jwt
import arrow
import requests
from bson import ObjectId


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

    @login_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=unicode, required=True)
        parser.add_argument('authority_url', type=unicode, required=True)
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
            authority_url=args['authority_url'],
            questions=questions,
            author=current_user.user
        )
        survey.save()

        register_token = jwt.encode({
            'iss': current_app.config['BASE_URL'],
            'survey_id': str(survey.id),
            'survey_name': survey.name
        }, current_app.config['PRIVATE_KEY'], algorithm='RS256')

        return {
            'survey': marshal(survey, survey_fields),
            'register_token': register_token
        }


class SurveyResource(Resource):
    @marshal_with(survey_fields)
    def get(self, survey_id):
        survey = Survey.objects.with_id(survey_id)
        return survey


class SurveyAnswerReport(Resource):
    @login_required
    def get(self, survey_id):
        survey = Survey.objects.with_id(survey_id)
        if not current_user.is_admin() and survey.author.id != current_user.get_id():
            return abort(401)

        answers = list(Answer.objects.aggregate(
            {'$match': {'survey': ObjectId(survey_id)}},
            {'$unwind': '$answers'},
            {'$group': {'_id': '$answers.question', 'answers': {'$push': '$answers.answer'}}}
        ))

        return answers
