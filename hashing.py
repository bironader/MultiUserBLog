import hmac
import hashlib

SECRET = 'valar morghulis'


def hash(user):
    return hmac.new(SECRET, user).hexdigest()


# take user_id and encode to cookie
def encode_cookie(user_key):
    # cookie = 2000| sdhasddw18w7d8q89151
    secure_cookie = "%s|%s" % (user_key, hash(user_key))
    return secure_cookie


def decode_cookie(cookie):  # take the cookie and return user_id
    user_key = cookie.split('|')[0]
    if cookie == encode_cookie(user_key):
        return user_key  # user_key = 2000


# take password ,username and salt to encode the user password
def encode_password(password, username, salt):
    datastore_password = hashlib.sha256(password + username + salt).hexdigest()
    return '%s|%s' % (salt, datastore_password)


# take the encoded password , username
def decode_password(password, username, datastore_password):
    # and the password come from user
    salt = datastore_password.split('|')[0]
    if datastore_password == encode_password(password, username, salt):
        return True
    else:
        return False
