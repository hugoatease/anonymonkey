var React = require('react');
var Link = require('react-router').Link;

var Home = React.createClass({
    render: function() {
        if (!this.props.authenticated) {
            var actionPanel = (
                <div className="panel panel-primary">
                    <div className="panel-heading">Login</div>
                    <div className="panel-body">
                        <p>Login or register an account on our OpenID Connect server to start or manage surveys.</p>
                        <p className="text-center"><a href="/login" className="btn btn-success">Login</a></p>
                    </div>
                </div>
            );
        }
        else {
            var actionPanel = (
                <div className="panel panel-primary">
                    <div className="panel-heading">Welcome {this.props.user.first_name} {this.props.user.last_name}</div>
                    <div className="panel-body">
                        <p>Create, share or manage your surveys here.</p>
                        <Link to="/create" className="btn btn-primary">Create survey</Link>
                        &nbsp;&nbsp;
                        <Link to="/surveys" className="btn btn-primary">Manage surveys</Link>
                    </div>
                </div>
            );
        }

        return (
            <div className="row">
                <div className="col-md-8">
                    <p className="lead">Welcome to Anonymonkey</p>
                    <p>
                        Anonymonkey is a survey platform offering anonymity for your user's panel.
                    </p>
                </div>
                <div className="col-md-4">
                    {actionPanel}
                </div>
            </div>
        );
    }
});

module.exports = Home;