var React = require('react');
var ReactDOM = require('react-dom');
var Router = require('react-router').Router;
var Route = require('react-router').Route;
var IndexRoute = require('react-router').IndexRoute;
var browserHistory = require('react-router').browserHistory;

var SurveyEdit = require('./SurveyEdit');

var App = React.createClass({
    render: function() {
        return (
            <div className="container">
                {this.props.children}
            </div>
        )
    }
});

module.exports = function(container) {
    ReactDOM.render((
        <Router history={browserHistory}>
            <Route path="/" component={App}>
                <IndexRoute component={SurveyEdit} />
            </Route>
        </Router>
    ), container);
};