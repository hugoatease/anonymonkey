from flask_restful import Api
from .survey import SurveyResource

api = Api()
api.add_resource(SurveyResource, '/api/surveys')
