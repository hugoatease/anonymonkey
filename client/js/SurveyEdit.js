var React = require('react');
var Survey = require('react-surveys');
var request = require('superagent');

var SurveyEdit = React.createClass({
    getInitialState: function() {
        return {
            survey: null
        };
    },

    componentDidMount: function() {
        if (this.props.params.survey_id) {
            request.get('/api/surveys/' + this.props.params.survey_id)
                .end(function(err, res) {
                    if (err) return;
                    this.setState({survey: res.body});
                }.bind(this));
        }
    },

    edit: function(survey) {
        request.post('/api/surveys')
            .send(survey)
            .end(function(err, res) {
                if (err) return;
                console.log(res.body);
            });
    },

    render: function() {
        return <Survey editing={true} survey={this.state.survey} surveyCallback={this.edit} />;
    }
});

module.exports = SurveyEdit;