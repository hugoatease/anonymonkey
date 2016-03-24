var React = require('react');
var ReactDOM = require('react-dom');
var Router = require('react-router').Router;
var Route = require('react-router').Route;
var IndexRoute = require('react-router').IndexRoute;
var browserHistory = require('react-router').browserHistory;
var merge = require('lodash/merge');
var clone = require('lodash/clone');
var Link = require('react-router').Link;

var Home = require('./Home');
var SurveyEdit = require('./SurveyEdit');
var SurveyAnswer = require('./SurveyAnswer');
var SurveyList = require('./SurveyList');

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

var NotFound = React.createClass({
   render: function() {
       return (
           <div>
               <h3>Route not found</h3><hr />
               <p>Please check the requested URL or <Link to="/">go back to homepage</Link>.</p>
               <img src="/static/404.gif" />
           </div>
       )
   }
});

function componentFactory(component, userProps) {
    return React.createClass({
        render: function() {
            var props = {};
            merge(props, this.props);
            merge(props, userProps);
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
                <Route path="/surveys" component={componentFactory(SurveyList, props)} />
                <Route path="*" component={NotFound} />
            </Route>
        </Router>
    ), container);
};