from google.appengine.ext import db
import hashing


# every blog containt subject artical , date , username ,userid
class BlogModel(db.Model):
    subject = db.StringProperty(required=True)
    artical = db.TextProperty(required=True)
    created = db.DateProperty(auto_now_add=True)
    user_id = db.StringProperty(required=True)
    user_name = db.StringProperty(required=True)


# every user has name , email , password
class UserModel(db.Model):
    user_name = db.StringProperty(required=True)
    email = db.StringProperty(required=True)
    password = db.StringProperty(required=True)

    # if user name exist get the passsword from datastore and match
    #  it with the entered password
    @classmethod
    def login(cls, username, password):
        u = cls.all().filter('user_name   =',
                             username).get()
        if u is not None:
            datastore_password = u.password
            if hashing.decode_password(password,
                                       username,
                                       datastore_password):
                return u
            else:
                return None
        else:
            return None


# every record contain post_id , comment , username, userid
class CommentModel(db.Model):
    blog_id = db.StringProperty()
    content = db.TextProperty(required=True)
    user_name = db.StringProperty(required=True)
    user_id = db.StringProperty(required=True)

    # every record contain post_id and number of likes on it


class LikeModel(db.Model):
    blog_id = db.StringProperty()
    number_likes = db.IntegerProperty()

    # every record contain userid and postid and boolean var


# if user like this post it will true else false
class UserLikes(db.Model):
    user_id = db.StringProperty()
    blog_id = db.StringProperty()
    boolean = db.BooleanProperty(default=False)
