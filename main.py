import os
import re
import webapp2
from google.appengine.ext import db
import jinja2
import string
import random
import datastore
import validation
import hashing
import datetime

JINJA_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader
(os.path.dirname(__file__) + "/templates"),
                               autoescape=True)

Error = False
PASSWORD_SALT = ''.join(random.choice(string.letters) for x in xrange(5))


def render_str(template, **params):
    t = JINJA_ENV.get_template(template)
    return t.render(params)


class BaseHandler(webapp2.RequestHandler):
    def render(self, template, **kw):
        self.response.out.write(render_str(template, **kw))

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def get_userid(self):  # get cookie (user_id)
        # then decode it to get the userid
        user_cookie = self.request.cookies.get('user_id')
        user_id = hashing.decode_cookie(user_cookie)
        return user_id

    def get_username(self):  # from user_id
        # we can get username
        if self.is_logged_in():
            key = db.Key.from_path('UserModel', long(self.get_userid()))
            user = db.get(key)
            user_name = user.user_name
            return user_name

    # Function check if the user is logged in or not
    def is_logged_in(self):
        is_login = self.request.cookies.get('user_id')
        if is_login is None:
            return False
        else:
            return True

            # Function redirect_user with some valdations :
            # if the user logged in cant redirect to the login form
            # if the user logged in cant redirect to register form
            # if the user not logged in cant post blog

    def redirect_user(self):
        current_url = self.request.url
        x = current_url.split('/')
        if self.is_logged_in() and x[3] == 'signup':
            self.render('Msg.html', msg="You already logged in",
                        is_logged_in=self.is_logged_in())
            return True
        elif self.is_logged_in() and x[3] == 'signin':
            self.render('Msg.html', msg="You already logged in",
                        is_logged_in=self.is_logged_in())
            return True
        elif not self.is_logged_in() and x[3] == 'newblog':
            self.redirect('/signin')
            return True
        elif not self.is_logged_in() and x[3] == 'home':
            self.redirect('/welcome')
            return True
        elif not self.is_logged_in() and x[3] == 'myposts':
            self.redirect('/signin')
            return True

    def add_cookie(self, name, user, expire):  # when user login add his id
        # to cookie and start session
        user_cookie = hashing.encode_cookie(str(user.key().id()))

        if not expire:  # if user check rembmer me
            # the the cookie will end in 2050
            self.response.headers.add_header('Set-Cookie',
                                             '%s=%s; Expires=Sun, '
                                             '15 Jul 2050 00:00:01 GMT Path=/' % (
                                                 name, user_cookie))

        else:
            self.response.headers.add_header('Set-Cookie',
                                             '%s=%s; Path=/' %
                                             (name, user_cookie))
        return user_cookie


class MainHandler(BaseHandler):
    def get(self):
        blog = db.GqlQuery("SELECT * FROM BlogModel")
        likes = db.GqlQuery("SELECT * FROM LikeModel")
        like = db.GqlQuery("SELECT * FROM UserLikes")
        users = db.GqlQuery("SELECT * FROM UserModel")
        db.delete(like)
        db.delete(likes)
        db.delete(users)
        db.delete(blog)


class WelcomePage(BaseHandler):
    def get(self):
        self.render('Welcome.html',
                    is_logged_in=self.is_logged_in(),
                    user_name=self.get_username())


class Msg(BaseHandler):  # error msg appear when user try to access login url
    # or signup url and he already logged in
    def get(self):
        self.render('Msg.html', is_logged_in=self.is_logged_in())


class FrontPage(BaseHandler):  # home page handler

    def get(self):
        if not self.redirect_user():
            is_liked = []
            blogs_id = []
            users_id = []
            # get blogs from database and render it to template
            blogs = db.GqlQuery(
                "SELECT * FROM BlogModel ORDER BY created DESC")
            # get comments from database and render it to template
            comments = db.GqlQuery("SELECT * FROM CommentModel")
            # get comments from database and render it to template
            likes = db.GqlQuery("SELECT * FROM LikeModel")
            user_likes = db.GqlQuery("SELECT *FROM UserLikes")
            for p in user_likes:
                is_liked.append(p.boolean)
                blogs_id.append(p.blog_id)
                users_id.append(p.user_id)

            is_liked.reverse()
            blogs_id.reverse()  # reserve all this list to pop
            users_id.reverse()  # it in jinja with the order of blogs
            self.render('FrontPage.html', blogs=blogs,
                        BlogModel=datastore.BlogModel,
                        is_logged_in=self.is_logged_in(),
                        comments=comments, CommentModel=datastore.CommentModel,
                        user_id=self.get_userid(),
                        likes=likes, LikeModel=datastore.LikeModel,
                        blogs_id=blogs_id,
                        users_id=users_id,
                        is_liked=is_liked)

            if (users_id):
                self.response.write(blogs_id)
                self.response.write(is_liked)
                self.response.write(users_id)

    def post(self):
        # determine if user click on post comment button
        comment = self.request.get('comment')
        blog_id = self.request.get('blog-id')
        # determine if user click on like button
        onClickLike = self.request.get('onClickLike')
        # determine if user click on editblog button
        onClickEdit = self.request.get('edit-blog')
        # determine if user click on delete blog button
        onClickDelete = self.request.get('delete-blog')
        # determine if user click on edit comment button
        onclickEditComment = self.request.get('edit-comment')
        # determine if user click on delete comment  button
        onClickDeleteComment = self.request.get('delete-comment')
        # determine if user click on unlike blog button
        onClickUnLike = self.request.get('onClickUnLike')

        if onClickLike:
            like = db.GqlQuery("SELECT * FROM LikeModel"
                               " WHERE blog_id =:1", blog_id)

            user_like = db.GqlQuery("SELECT * FROM UserLikes "
                                    "WHERE blog_id =:1 "
                                    "and user_id=:2", blog_id,
                                    self.get_userid())
            if like.get() is None:
                current_likes = 1
                like = datastore.LikeModel(blog_id=blog_id,
                                           number_likes=current_likes)
                like.put()
                user_likes = datastore.UserLikes(user_id=self.get_userid(),
                                                 blog_id=blog_id, boolean=True)
                user_likes.put()

            else:
                current_likes = like.get().number_likes + 1
                like = like.get()
                like.number_likes = current_likes
                like.put()
                user_like = user_like.get()
                user_like.boolean = True
                user_like.put()

        if onClickUnLike:
            self.response.write("hi")
            like = db.GqlQuery("SELECT * FROM LikeModel WHERE"
                               " blog_id =:1", blog_id)
            user_like = db.GqlQuery("SELECT * FROM UserLikes "
                                    "WHERE blog_id =:1 and user_id=:2", blog_id,
                                    self.get_userid())
            current_likes = like.get().number_likes - 1
            like = like.get()
            like.number_likes = current_likes
            like.put()
            user_like = user_like.get()
            user_like.boolean = False
            user_like.put()

        if comment:  # Comment on Post
            comment_blog = datastore.CommentModel(content=comment,
                                                  user_name=self.get_username(),
                                                  user_id=self.get_userid(), blog_id=blog_id)
            comment_blog.put()

        if onClickEdit:  # Edit Post
            subject = self.request.get('edit-subject')
            artical = self.request.get('edit-artical')
            key = db.Key.from_path('BlogModel', long(blog_id))
            new_post = db.get(key)
            if new_post:
                new_post.subject = subject
                new_post.artical = artical
                new_post.put()

        if onClickDelete:  # Delete Post
            key = db.Key.from_path('BlogModel', long(blog_id))
            old_post = db.get(key)
            comments = db.GqlQuery("SELECT * FROM CommentModel"
                                   " WHERE blog_id =:1", blog_id)

            likes = db.GqlQuery("SELECT * FROM LikesModel"
                                " WHERE blog_id =:1", blog_id)

            user_likes = db.GqlQuery("SELECT * FROM UserLikes"
                                     " WHERE blog_id =:1", blog_id)
            if old_post:
                db.delete(old_post)
                db.delete(comments)
                db.delete(user_likes)
                db.delete(likes)

        if onclickEditComment:  # Edit comment
            edit_comment = self.request.get('edit-comment')
            comment_id = self.request.get('comment-id')
            key = db.Key.from_path('CommentModel', long(comment_id))
            new_comment = db.get(key)
            if new_comment:
                new_comment.content = edit_comment
                new_comment.put()

        if onClickDeleteComment:  # Delete Comment
            comment_id = self.request.get('comment-id')
            key = db.Key.from_path('CommentModel', long(comment_id))
            old_comment = db.get(key)
            if old_comment:
                db.delete(old_comment)

        self.redirect('/home')


class BlogPost(BaseHandler):  # blog form handler
    def get(self, blog_key):
        key = db.Key.from_path('BlogModel', long(blog_key))
        post = db.get(key)
        self.render('Post.html', post=post, is_logged_in=self.is_logged_in())


class BlogForm(BaseHandler):  # Blog form page handler
    def get(self):
        if not self.redirect_user():
            self.render('BlogForm.html',
                        is_logged_in=self.is_logged_in())

    def post(self):
        subject = self.request.get('subject')
        artical = self.request.get('textarea')
        if subject and artical:
            blog = datastore.BlogModel(subject=subject,
                                       artical=artical,
                                       user_id=self.get_userid(),
                                       user_name=self.get_username())
            blog.put()  # add blog
            self.redirect('/%s' % blog.key().id())

        # Validation stuff
        elif subject and not artical:
            self.render('BlogForm.html',
                        errorblog="Enter Blog",
                        is_logged_in=self.is_logged_in())
        elif artical and not subject:
            self.render('BlogForm.html',
                        errorsub="Enter Subject",
                        is_logged_in=self.is_logged_in())
        else:
            self.render('BlogForm.html', errorsub="Enter Subject",
                        errorblog="Enter Blog",
                        is_logged_in=self.is_logged_in())


class MyPosts(BaseHandler):
    def get(self):
        if not self.redirect_user():
            blogs = db.GqlQuery("SELECT * FROM BlogModel WHERE "
                                "user_id =:1", self.get_userid())
            comments = db.GqlQuery("SELECT * FROM CommentModel")
            self.render('FrontPage.html',
                        blogs=blogs,
                        BlogModel=datastore.BlogModel,
                        is_logged_in=self.is_logged_in(),
                        comments=comments, CommentModel=datastore.CommentModel)


class RegistrationForm(BaseHandler):  # signup form handler
    def get(self):
        if not self.redirect_user():
            self.render('RegistrationForm.html',
                        is_logged_in=self.is_logged_in())

    # register with validations
    def post(self):
        if not self.is_logged_in():
            global Error
            username = self.request.get('username')
            password = self.request.get('password')
            conf_passowrd = self.request.get('password_confirm')
            email = self.request.get('email')

            params = dict()

            if not validation.valid_user(username=username):
                params['usererror'] = "Username must be unique and can contain any letters " \
                                      "or numbers, without spaces."
                Error = True

            if not validation.valid_password(password=password):
                params['passworderror'] = "Password should be " \
                                          "at least 4 characters."
                Error = True

            if conf_passowrd != password:
                params['confirmerror'] = "Your passwords didn't match."
                Error = True

            if not validation.valid_email(email=email):
                params['emailerror'] = "That's not a valid email."
                Error = True

            if Error:
                self.render('RegistrationForm.html', **params)
            else:
                password = hashing.encode_password(password,
                                                   username,
                                                   PASSWORD_SALT)

                user = datastore.UserModel(user_name=username,
                                           email=email,
                                           password=password)
                user.put()  # user Register
                self.redirect('/signin')  # link to login form


class Login(BaseHandler):  # Login handler form
    def get(self):
        if not self.redirect_user():
            self.render('Login.html',
                        is_logged_in=self.is_logged_in())

    def post(self):
        if not self.is_logged_in():
            username = self.request.get('username')
            password = self.request.get('password')
            remember_me = self.request.get('remember')
            user = datastore.UserModel.login(username=username,
                                             password=password)
            if user:
                if remember_me:
                    self.add_cookie('user_id', user, False)

                else:
                    self.add_cookie('user_id', user, True)

                self.redirect('/welcome')

            else:
                self.render('Login.html',
                            error_login="username or password is incorrect")


class Logout(BaseHandler):  # logout and remove user_id
    #  cookie to end the session
    def logout(self):
        self.response.set_cookie("user_id", None)

    def get(self):
        if self.is_logged_in():
            self.logout()
            self.redirect('/welcome')


app = webapp2.WSGIApplication([
    ('/newblog', BlogForm), ('/home', FrontPage),
    ('/signup', RegistrationForm), ('/signin', Login),
    ('/', MainHandler), ('/error', Msg),
    ('/logout', Logout),
    (r'/([0-9]+)', BlogPost),
    ('/welcome', WelcomePage),
    ('/myposts', MyPosts)
], debug=True)
