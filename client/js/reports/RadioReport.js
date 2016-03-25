var React = require('react');
var find = require('lodash/find');
var countBy = require('lodash/countBy');
var identity = require('lodash/identity');

var RadioReport = React.createClass({
    render: function() {
        var counts = countBy(this.props.answers, identity);
        return (
            <ul className="list-group">
                {this.props.question.options.map(function(option) {
                    return (
                        <li className="list-group-item">
                            <span className="badge">{counts[option.id]}</span>
                            {option.name}
                        </li>
                    );
                })}
            </ul>
        );
    }
});

module.exports = RadioReport;