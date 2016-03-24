var React = require('react');
var Survey = require('react-surveys');
var request = require('superagent');

var SurveyAnswer = React.createClass({
    getInitialState: function() {
        return {
            survey: null
        }
    },

    componentDidMount: function() {
        request.get('/api/surveys/' + this.props.params.survey_id)
            .end(function(err, res) {
                if (err) return;
                console.log(res.body);
                this.setState({survey: res.body});
            }.bind(this));
    },

    render: function() {
        if (this.state.survey) {
            return <Survey editing={false} survey={this.state.survey} />;
        }
        else {
            return <div>Loading survey...</div>;
        }
    }
});

module.exports = SurveyAnswer;