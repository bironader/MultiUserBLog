import os
import re
from google.appengine.ext import db
import datastore

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')


def valid_user(username):
    u = datastore.UserModel.all().filter('user_name   =', username).get()
    if not username or USER_RE.match(username) is None:
        return False
    elif u is not None:
        return False
    else:
        return True


def valid_password(password):
    if not password or PASS_RE.match(password) is None:
        return False
    else:
        return True


def valid_email(email):
    if not email or EMAIL_RE.match(email) is None:
        return False
    else:
        return True
