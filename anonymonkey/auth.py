from flask import redirect, url_for, request
from flask_login import UserMixin, LoginManager
from .schemas import User

login_manager = LoginManager()


class UserHandler(UserMixin):
    def __init__(self, user):
        self.user = user

    def get_id(self):
        return self.user.sub

    def is_admin(self):
        return self.user.admin

    def serialize(self):
        return {
            'sub': self.user.sub,
            'email': self.user.email,
            'admin': self.user.admin,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'id_token': self.user.id_token
        }


@login_manager.user_loader
def load_user(user_sub):
    return UserHandler(User.objects.with_id(user_sub))


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login', next=request.path))