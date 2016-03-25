var React = require('react');
var ReactDOM = require('react-dom');
var Chart = require('chart.js');
var keys = require('lodash/keys');
var find = require('lodash/find');
var randomcolor = require('randomcolor');

var ChartView = React.createClass({
    getDefaultProps: function() {
        return {
            width: 200,
            height: 200
        };
    },

    componentDidMount: function() {
        var ctx = ReactDOM.findDOMNode(this.refs.chart).getContext("2d");
        var data = keys(this.props.counts).map(function(option_id) {
            return {
                value: this.props.counts[option_id],
                label: find(this.props.options, {id: option_id}).name,
                color: randomcolor()
            }
        }.bind(this));
        new Chart(ctx).Doughnut(data, {responsive: true});
    },

    render: function() {
        return <canvas ref="chart" width={this.props.width} height={this.props.height} />;
    }
});

module.exports = ChartView;