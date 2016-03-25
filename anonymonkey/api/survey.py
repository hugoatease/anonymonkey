from flask import request, current_app, render_template, url_for, jsonify
from flask_restful import Resource, reqparse, marshal_with, abort
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


class SurveyShareResource(Resource):
    @login_required
    def post(self, survey_id):
        survey = Survey.objects.with_id(survey_id)
        if survey.author.id != current_user.get_id():
            return abort(401)

        parser = reqparse.RequestParser()
        parser.add_argument('email', type=unicode, required=True)
        args = parser.parse_args()

        survey.update(push__recipients=args['email'])

        token = jwt.encode({
            'iss': current_app.config['TOKEN_ISSUER'],
            'iat': arrow.utcnow().datetime,
            'survey_id': str(survey.id)
        }, current_app.config['SECRET_KEY'])

        url = url_for('index_all', path='/survey/' + str(survey.id), _external=True) + '?token=' + token
        html = render_template('email.html', survey_name=survey.name, url=url)

        req = requests.post('https://api.mailgun.net/v3/' + current_app.config['MAILGUN_DOMAIN'] + '/messages', data={
            'from': current_app.config['MAIL_SENDER'],
            'to': args['email'],
            'subject': survey.name + ' survey invitation',
            'html': html,
            }, auth=('api', current_app.config['MAILGUN_KEY']))

        print req.content

        return jsonify({'error': False, 'email': args['email']})


class SurveyAnswerReport(Resource):
    @login_required
    def get(self, survey_id):
        answers = list(Answer.objects.aggregate(
            {'$match': {'survey': ObjectId(survey_id)}},
            {'$unwind': '$answers'},
            {'$group': {'_id': '$answers.question', 'answers': {'$push': '$answers.answer'}}}
        ))

        return answers
