from flask import current_app
from flask_restful import Resource, reqparse, marshal_with, abort
from anonymonkey.schemas import Survey, Answer, AnswerItem, TokenBlacklist
from .fields import answer_fields
import jwt


class AnswerListResource(Resource):
    @marshal_with(answer_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=unicode, required=True)
        parser.add_argument('answers', type=list, location='json')
        args = parser.parse_args()

        if TokenBlacklist.objects(token=args['token']).first() is not None:
            return abort(401)

        survey_id = jwt.decode(args['token'],
                               current_app.config['SECRET_KEY'],
                               issuer=current_app.config['TOKEN_ISSUER']
                               )['survey_id']

        print survey_id

        survey = Survey.objects.with_id(survey_id)

        def create_item(answer):
            return AnswerItem(
                question=answer['question'],
                answer=answer['answer']
            )

        answers = map(create_item, args['answers'])

        answer = Answer(
            survey=survey,
            answers=answers
        )

        answer.save()

        blacklist = TokenBlacklist(token=args['token'])
        blacklist.save()

        return answer
