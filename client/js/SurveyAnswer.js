var React = require('react');
var Survey = require('react-surveys');
var request = require('superagent');
var swal = require('sweetalert');

var SurveyAnswer = React.createClass({
    getInitialState: function() {
        return {
            survey: null
        }
    },

    componentDidMount: function() {
        request.get('/api/surveys/' + this.props.params.survey_id)
            .end(function(err, res) {
                if (err)  {
                    swal('Survey error', 'Unable to fetch survey', 'error');
                    return;
                }
                this.setState({survey: res.body});
            }.bind(this));
    },

    onAnswers: function(answers) {
        request.post('/api/answers')
            .send({
                survey_id: this.props.params.survey_id,
                token: this.props.location.query.token,
                answers: answers.answers
            })
            .end(function(err, res) {
                if (err) {
                    swal('Survey error', 'Unable to submit your answers. Maybe you already answered the survey.', 'error');
                    return;
                }
                swal('Survey submitted', 'Your answers have been submitted. Thank you !', 'success');
            }.bind(this));
    },

    render: function() {
        if (this.state.survey) {
            return <Survey editing={false} survey={this.state.survey} answersCallback={this.onAnswers} />;
        }
        else {
            return <div>Loading survey...</div>;
        }
    }
});

module.exports = SurveyAnswer;