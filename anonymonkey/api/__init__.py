from flask_restful import Api
from .survey import SurveyListResource, SurveyResource, SurveyAnswerReport
from .answer import AnswerListResource

api = Api()
api.add_resource(SurveyListResource, '/api/surveys')
api.add_resource(SurveyResource, '/api/surveys/<survey_id>')
api.add_resource(AnswerListResource, '/api/answers')
api.add_resource(SurveyAnswerReport, '/api/surveys/<survey_id>/report')
