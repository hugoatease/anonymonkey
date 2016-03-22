from flask_restful import Resource, reqparse, marshal_with
from .fields import survey_fields
from anonymonkey.schemas import Survey, Question, QuestionOption


class SurveyResource(Resource):
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
            questions=questions
        )

        survey.save()
        return survey