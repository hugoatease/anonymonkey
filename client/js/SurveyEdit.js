var React = require('react');
var Survey = require('react-surveys');
var request = require('superagent');
var clone = require('lodash/clone');

var SurveyEdit = React.createClass({
    getInitialState: function() {
        return {
            survey: null,
            authority_url: null
        };
    },

    componentDidMount: function() {
        if (this.props.params.survey_id) {
            request.get('/api/surveys/' + this.props.params.survey_id)
                .end(function(err, res) {
                    if (err) return;
                    this.setState({survey: res.body});
                    this.setState({authority_url: res.body.authority_url});
                }.bind(this));
        }
    },

    edit: function(survey) {
        survey.authority_url = this.state.authority_url;
        request.post('/api/surveys')
            .send(survey)
            .end(function(err, res) {
                if (err) return;
                request.post(this.state.authority_url + '/api/surveys')
                    .set('Authorization', 'JWT ' + this.props.user.id_token)
                    .send({survey_id: res.body.id})
                    .end();
            }.bind(this));
    },

    onAuthorityChange: function(ev) {
        this.setState({authority_url: ev.target.value});
    },

    render: function() {
        return (
            <div>
                <input type="text" className="form-control" value={this.state.authority_url} onChange={this.onAuthorityChange} />
                <Survey editing={true} survey={this.state.survey} surveyCallback={this.edit} />
            </div>
        );
    }
});

module.exports = SurveyEdit;