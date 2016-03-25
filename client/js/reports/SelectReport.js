var React = require('react');
var find = require('lodash/find');
var countBy = require('lodash/countBy');
var identity = require('lodash/identity');
var ChartView = require('./ChartView');

var SelectReport = React.createClass({
    render: function() {
        var counts = countBy(this.props.answers, identity);
        return (
            <div>
                <ChartView counts={counts} options={this.props.question.options} />
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
            </div>
        );
    }
});

module.exports = SelectReport;