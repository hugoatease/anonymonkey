# Anonymonkey

Anonymonkey is an attempt at creating an anonymous survey mechanism.
Surveyors hosts their questions on a web service which allows users belonging
to a panel to answer anonymously.

This system relies on an external survey authority where members of the panel
can exchange a mail-transmitted JWT token with another token containing no
identity information. JWT are used to make a public-key based assertion
of the grant of the survey authority to answer the survey.

Survey edition uses the [react-surveys](https://github.com/hugoatease/react-surveys)
library UI and survey format.

Documentation
--------------
Survey service API documentation is available at [docs.anonymonkey.apiary.io](http://docs.anonymonkey.apiary.io/).

Survey authority API documentation can be found at [docs.anonymonkey-authority.apiary.io](http://docs.anonymonkey-authority.apiary.io/).

Features
---------
- Survey creation, with a reactive edition UI
- Survey sharing via email
- Anonymity based on the JWT payload disclosure
- Survey answers reporting
- REST APIs for survey edition, answering and reporting
- Dynamic discovery of survey authorities
- OpenID Connect authentication

Dependencies
------------
Anonymonkey uses MongoDB as a datastore for survey, answers and token blacklist.
Redis is used for temporary data storage and discovery data caching.

Since Anonymonkey authenticates users through OpenID Connect and JWTs, an OpenID
Connect compliant authentication server is needed for it to run properly.

Anonymonkey is tested to authenticate through [Yoshimi](https://github.com/hugoatease/yoshimi),
but it should work with others third-party OpenID Connect providers (Google
accounts, [Keycloak](http://keycloak.jboss.org)...).

A survey authority web service needs to be hosted in order for Anonymonkey
to work. Setup instructions can be found on
[anonymonkey-authority](https://github.com/hugoatease/anonymonkey-authority)
repository.

Email sending is handled by [Mailgun](http://www.mailgun.com/). Mailgun allows to send emails reliably without the use of a SMTP server.

Configuration and setup
============
## Quick start

Anonymonkey is hosted on [anonymonkey.caille.me](http://anonymonkey.caille.me),
alongside with the authority service on `http://authority.caille.me`.

A `docker-compose.yml` file is present in the repository, allowing the
whole service to be started on a local machine using

    docker-compose up

Anonymonkey service is exposed to the Docker host on port `8000`, and
authority service on port `8080`.

If you're running [Docker Toolbox](https://www.docker.com/products/docker-toolbox)
on OSX or Windows instead of running Docker on Linux directly, you should
change `BASE_URL` in `docker/settings_main.py` to `http://192.168.99.100:8000`.

Configuration files for the two services are to be found in the `docker/`
directory.

## Configuration reference
Anonymonkey service configuration is stored in the `settings.py` file.

Before going into production, you must change the sample settings by
providing values for the variables below.

| Parameter name                    | Description                |
|:----------------------------------|:---------------------------|
| `DEBUG`                           | Should the application be in debug mode. Set this to False in production |
| `SECRET_KEY`                      | Random characters string used to cryptographically sign important information such as cookies and JWTs |
| `MONGODB_DB`                      | MongoDB database name |
| `MONGODB_HOST` | MongoDB server hostname |
| `MONGODB_PORT` | MongoDB server port |
| `REDIS_HOST` | Redis server hostname |
| `REDIS_PORT` | Redis server port |
| `OPENID_CLIENT`                       | OpenID Connect OAuth client ID |
| `OPENID_SECRET`                   | OpenID Connect OAuth secret |
| `OPENID_REDIRECT`                    | OpenID Connect redirect_uri. Must point to /login_return |
| `OPENID_AUTHORIZE_ENDPOINT` | OpenID Connect authorization URL |
| `OPENID_TOKEN_ENDPOINT` | OpenID Connect token endpoint |
| `OPENID_USERINFO_ENDPOINT` | OpenID Connect UserInfo endpoint |
| `OPENID_ISSUER_KEY` | OpenID server public key used to sign JWT assertions |
| `OPENID_ISSUER_CLAIM` | JWT issuer claim of OpenID Connect server |
| `BASE_URL` | JWT issuer used in survey registration tokens |
| `PRIVATE_KEY` | Private RSA key used to sign JWTs |
| `PUBLIC_KEY` | Public RSA key used to sign JWTs |

### Manual setup
Python and Gunicorn are used to host the backend service. Node.js and Gulp are
required to compile static assets.

These commands assume you have active MongoDB and Redis server listening on
local host.

    git clone https://github.com/hugoatease/anonymonkey.git
    cd anonymonkey
    virtualenv env
    source env/bin/activate
    pip install -r requirements.txt
    pip install gunicorn
    npm install -g gulp
    npm install
    gulp
    gunicorn anonymonkey:app

License
============
© 2016 Hugo Caille & Aymeric Masse.

Anonymonkey is released upon the terms of the Apache 2.0 License.
