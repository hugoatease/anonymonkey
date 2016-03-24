var React = require('react');
var ReactDOM = require('react-dom');
var Router = require('react-router').Router;
var Route = require('react-router').Route;
var IndexRoute = require('react-router').IndexRoute;
var browserHistory = require('react-router').browserHistory;

var Home = require('./Home');
var SurveyEdit = require('./SurveyEdit');
var SurveyAnswer = require('./SurveyAnswer');

var App = React.createClass({
    render: function() {
        return (
            <div>
                <nav className="navbar navbar-default">
                  <div className="container-fluid">
                    <div className="navbar-header">
                      <a class="navbar-brand" href="#">
                        <img alt="Anonymonkey" src="/static/logo.png" height="50"/>
                      </a>
                    </div>
                  </div>
                </nav>
                <div className="container">
                    {this.props.children}
                </div>
            </div>
        )
    }
});

function componentFactory(component, props) {
    return React.createClass({
        render: function() {
            return React.createElement(component, props);
        }
    });
}

module.exports = function(container, props) {
    ReactDOM.render((
        <Router history={browserHistory} {...props}>
            <Route path="/" component={App}>
                <IndexRoute component={componentFactory(Home, props)} />
                <Route path="/create" component={componentFactory(SurveyEdit, props)} />
                <Route path="/survey/:survey_id" component={componentFactory(SurveyAnswer, props)} />
                <Route path="/survey/:survey_id/edit" component={componentFactory(SurveyEdit, props)} />
            </Route>
        </Router>
    ), container);
};