MONGODB_DB = 'anonymonkey'
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DEBUG = True
SECRET_KEY = 'WWRXEbMy78CIoYXjGaYIDS6P3RYB7GHWiknTSX8LEg8='
OPENID_CLIENT = 'ArXOM0Yy0LZM4qN05Lw2rCS1oDUUy68MPblzLuB6DE6KnitKF5DQZtqR'
OPENID_SECRET = 'PIkvoNlQqURZh9I-d0C0qR3yDue7XSM7AgjNdy4TqlfnSj7xn1W3CcHD'
OPENID_REDIRECT = 'http://localhost:8000/login/return'
OPENID_AUTHORIZE_ENDPOINT = 'https://www.wapitisen.fr/sso/oauth/authorize'
OPENID_TOKEN_ENDPOINT = 'https://www.wapitisen.fr/sso/oauth/token'
OPENID_USERINFO_ENDPOINT = 'https://www.wapitisen.fr/sso/oauth/userinfo'
OPENID_ISSUER_KEY = '''-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAuINbLPfPI10l+tzNpaMH
9Hwp63zKDNrEioMVpd0V5BG2m0+WaWjA47D+yEOzpbP1fK8440rTMmDBRiHyB2yj
M9QP+rz6gUfhE5O+F/Q887hpXf8GMgfSSyYPBVNYLa/7lRWK0Q3xUMLnwhlK9Ncc
E0k4VsLmHybcY36paV1388hAOM+H+7vv8yTX7bsvYcgshxpaUVUAQhb+ivQWMewm
kKxqbhFmrJscJE7WJZFBvT+R8MWH83hZaISAZHR92ZO+53CuPYFBsUxX4kk8f5Nd
DXZqdpmIfKgQmzLAzmLfICrPZF7gQlZk/lIpipdH1jjbgIgHXUq6RyKb6w1qhtw9
7QIDAQAB
-----END PUBLIC KEY-----'''
OPENID_ISSUER_CLAIM = 'https://www.wapitisen.fr'
TOKEN_ISSUER = 'http://www.anonymonkey.com/'
MAIL_SENDER = 'contact@anonymonkey.com'
MAILGUN_DOMAIN = 'sandboxb0aefc369dbb4e0f995e02c5d5b83310.mailgun.org'
MAILGUN_KEY = 'key-1708e9472fe78761013b20882a835a2c'