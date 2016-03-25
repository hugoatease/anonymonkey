var React = require('react');

var TextReport = React.createClass({
    render: function() {
        return (
            <ul className="list-group">
                {this.props.answers.map(function(answer) {
                    return <li className="list-group-item">{answer}</li>;
                })}
            </ul>
        );
    }
});

module.exports = TextReport;