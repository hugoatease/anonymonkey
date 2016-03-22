var React = require('react');
var Survey = require('react-surveys');
var request = require('superagent');

var SurveyEdit = React.createClass({
    edit: function(survey) {
        console.log(survey);
        request.post('/api/surveys')
            .send(survey)
            .end(function(err, res) {
                if (err) return;
                console.log(res.body);
            });
    },

    render: function() {
        return <Survey editing={true} surveyCallback={this.edit} />;
    }
});

module.exports = SurveyEdit;