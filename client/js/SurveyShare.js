var React = require('react');
var request = require('superagent');
var ReactDOM = require('react-dom');
var swal = require('sweetalert');

var SurveyShare = React.createClass({
    share: function(ev) {
        ev.preventDefault();
        var email = ReactDOM.findDOMNode(this.refs.email).value;

        request.post(this.props.authority_url + '/api/surveys/' + this.props.survey_id + '/share')
            .set('Authorization', 'JWT ' + this.props.id_token)
            .send({email: email})
            .end(function(err, res) {
                if (err) {
                    swal('Survey sharing', 'Unable to share survey to ' + email, 'error');
                    return;
                }
                swal('Survey sharing', 'Survey has been shared to ' + email, 'success');
            });
    },

    render: function() {
        return (
            <form onSubmit={this.share}>
                <div className="form-group">
                    <label>Recipient email</label>
                    <input className="form-control" type="text" placeholder="Recipient email" ref="email" />
                </div>
                <button className="btn btn-primary" type="submit">Share</button>
            </form>
        )
    }
});

module.exports = SurveyShare;