from flask import current_app, g
from flask_restful import Resource, reqparse, marshal_with, abort
from anonymonkey.schemas import Survey, Answer, AnswerItem, TokenBlacklist
from .fields import answer_fields
import jwt
import requests


def fetch_authority_key(survey):
    cached = g.redis.get('anonymonkey.authorities.public_key.' + survey.authority_url)
    if cached is None:
        discovery = requests.get(survey.authority_url + '/.well-known/anonymonkey').json()
        g.redis.set('anonymonkey.authorities.public_key.' + survey.authority_url, discovery['token_key']['pem']['public'])
        g.redis.expire('anonymonkey.authorities.public_key.' + survey.authority_url, 1800)
        return discovery['token_key']['pem']['public']
    else:
        return cached


class AnswerListResource(Resource):
    @marshal_with(answer_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('survey_id', type=unicode, required=True)
        parser.add_argument('token', type=unicode, required=True)
        parser.add_argument('answers', type=list, location='json')
        args = parser.parse_args()

        survey = Survey.objects.with_id(args['survey_id'])

        token = jwt.decode(
            args['token'],
            fetch_authority_key(survey),
            issuer=current_app.config['TOKEN_ISSUER'],
            algorithms='RS256'
        )

        if TokenBlacklist.objects(survey=survey, token=token['token']).first() is not None:
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

        blacklist = TokenBlacklist(survey=survey, token=token['token'])
        blacklist.save()

        return answer
