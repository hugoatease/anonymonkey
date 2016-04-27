var React = require('react');
var request = require('superagent');
var ReactDOM = require('react-dom');

var SurveyShare = React.createClass({
    share: function(ev) {
        ev.preventDefault();
        var email = ReactDOM.findDOMNode(this.refs.email).value;

        request.post(this.props.base_url + '/api/surveys/' + this.props.survey_id + '/share')
            .set('Authorization', 'JWT ' + this.props.id_token)
            .send({email: email})
            .end(function(err, res) {
                if (err) return;
            })
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