var React = require('react');
var request = require('superagent');
var Link = require('react-router').Link;
var SurveyShare = require('./SurveyShare');

var SurveyList = React.createClass({
    getInitialState: function() {
        return {
            surveys: []
        }
    },

    componentDidMount: function() {
        request.get('/api/surveys')
            .query({author: this.props.user.sub})
            .end(function(err, res) {
                if (err) return;
                this.setState({surveys: res.body});
            }.bind(this));
    },

    render: function() {
        return (
            <div className="row">
                <div className="col-md-6">
                    <h3>My surveys</h3><hr />
                    {this.state.surveys.map(function(survey) {
                        return (
                            <div className="panel panel-default">
                                <div className="panel-body">
                                    <h3>{survey.name}</h3>
                                    <p>{survey.description}</p>
                                    <Link to={'/survey/' + survey.id + '/edit'} className="btn btn-default">Edit survey</Link>
                                    &nbsp;&nbsp;
                                    <Link to={'/survey/' + survey.id + '/report'} className="btn btn-default">Answers report</Link>
                                    <SurveyShare survey_id={survey.id} />
                                </div>
                            </div>
                        );
                    })}
                </div>
            </div>
        );
    }
});

module.exports = SurveyList;