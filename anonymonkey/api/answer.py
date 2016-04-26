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

        token = jwt.decode(
            args['token'],
            current_app.config['AUTHORITY_KEY'],
            issuer=current_app.config['TOKEN_ISSUER'],
            algorithms='RS256'
        )

        survey = Survey.objects.with_id(token['survey_id'])

        if TokenBlacklist.objects(token=token['token']).first() is not None:
            return abort(401)

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

        blacklist = TokenBlacklist(token=token['token'])
        blacklist.save()

        return answer
