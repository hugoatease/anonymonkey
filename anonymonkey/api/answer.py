from flask_restful import Resource, reqparse, marshal_with
from anonymonkey.schemas import Survey, Answer, AnswerItem
from .fields import answer_fields


class AnswerListResource(Resource):
    @marshal_with(answer_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('survey', type=unicode, required=True)
        parser.add_argument('answers', type=list, location='json')
        args = parser.parse_args()

        def create_item(answer):
            return AnswerItem(
                question=answer['question'],
                answer=answer['answer']
            )

        answers = map(create_item, args['answers'])

        answer = Answer(
            survey=args['survey'],
            answers=answers
        )

        answer.save()
        return answer
