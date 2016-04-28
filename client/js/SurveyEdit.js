var React = require('react');
var Survey = require('react-surveys');
var request = require('superagent');
var clone = require('lodash/clone');
var validUrl = require('valid-url');
var browserHistory = require('react-router').browserHistory;
var swal = require('sweetalert');

var SurveyEdit = React.createClass({
    getInitialState: function() {
        return {
            survey: null,
            authority_url: null,
            authority_ok: false
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
                if (err) {
                    swal('Survey creation error', 'Unable to submit survey to the server', 'error');
                    return;
                }
                request.post(this.state.authority_url + '/api/surveys')
                    .set('Authorization', 'JWT ' + this.props.user.id_token)
                    .send({register_token: res.body.register_token})
                    .end(function(err, res) {
                        if (err) {
                            swal('Survey creation error', 'Unable to register survey on authority', 'error');
                            return;
                        }
                        browserHistory.push('/surveys');
                    }.bind(this));
            }.bind(this));
    },

    onAuthorityChange: function(ev) {
        this.setState({authority_url: ev.target.value});
        if (validUrl.isUri(ev.target.value)) {
            this.testAuthority(ev.target.value);
        }
        else {
            this.setState({authority_ok: false});
        }
    },

    testAuthority: function(url) {
        request.get(url + '/.well-known/anonymonkey-authority')
            .end(function(err, res) {
                if (err || !res.body || !res.body.token_key) {
                    this.setState({authority_ok: false});
                }
                else {
                    this.setState({authority_ok: true});
                }
            }.bind(this));
    },

    render: function() {
        var authority_status = (
            <div className="alert alert-danger">
                Please check authority URL before submitting survey
            </div>
        );

        if (this.state.authority_ok) {
            authority_status = (
                <div className="alert alert-success">
                    Authority URL is correct
                </div>
            );
        }

        return (
            <div>
                <h3>Survey authority</h3><hr />
                <p>
                    A survey authority ensures your panel's anonymity by managing survey authorizations away from survey
                    server.
                </p>
                {authority_status}
                <input type="text" className="form-control" value={this.state.authority_url}
                       onChange={this.onAuthorityChange} onBlur={this.testAuthority.bind(this, this.state.authority_url)} placeholder="Authority URL" />
                <Survey editing={true} survey={this.state.survey} surveyCallback={this.edit} />
            </div>
        );
    }
});

module.exports = SurveyEdit;