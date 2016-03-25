var React = require('react');
var request = require('superagent');
var find = require('lodash/find');
var keys = require('lodash/keys');
var inArray = require('in-array');
var reports = require('./reports');

var SurveyReport = React.createClass({
    getInitialState: function() {
        return {
            survey: null,
            report: []
        };
    },

    componentDidMount: function() {
        request.get('/api/surveys/' + this.props.params.survey_id)
            .end(function(err, res) {
                if (err) return;
                var survey = res.body;
                this.setState({survey: survey});

                request.get('/api/surveys/' + this.props.params.survey_id + '/report')
                    .end(function(err, res) {
                        if (err) return;
                        var answers = res.body.map(function(answer) {
                            var question = find(survey.questions, {id: answer._id});
                            return {
                                question: question,
                                answers: answer.answers
                            }
                        });
                        this.setState({report: answers});
                    }.bind(this));
            }.bind(this));
    },

    render: function() {
        console.log(this.state.report);
        if (!this.state.survey) {
            return <div>Loading survey...</div>;
        }
        else {
            return (
                <div>
                    <h3>Answers report <small>for {this.state.survey.name}</small></h3>
                    <div className="row">
                        {this.state.report.map(function(item) {
                            var report = null;
                            if (inArray(keys(reports), item.question.type)) {
                                report = React.createElement(reports[item.question.type], {
                                    answers: item.answers,
                                    question: item.question
                                });
                            }
                            return (
                                <div className="col-md-6 panel panel-default">
                                    <div className="panel-body">
                                        <h3>{item.question.name}</h3>
                                        <p>{item.question.description}</p>
                                        {report}
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                </div>
            );
        }
    }
});

module.exports = SurveyReport;