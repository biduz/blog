import main_handler
import json
import model
import user_stuff

class Index(main_handler.Handler):
    def get(self):
        posts = model.list_posts()
        self.render('index.html', posts = posts)

class PermaLink(main_handler.Handler):
    def get(self, post_id):
        post = model.post_by_id(post_id)
        if post:
            self.render('singlepost.html', post = post)
        else:
            self.redirect('/')

class NewPost(main_handler.Handler):
    def get(self):
        if self.user:
            self.render('newpost.html')
        else:
            self.redirect('/login?from_path=/newpost')

    def post(self):
        if not self.user:
            self.redirect('/login?from_path=/newpost')
        #TBD: be sure that the code below will not run after redirect
        subject = self.get_from_request('subject')
        content = self.get_from_request('content')

        if subject and content:
            post = model.new_post(subject = subject, content = content)
            self.redirect('posts/%s' % post)
        else:
            error = 'We need both the content and title of the post'
            self.render('newpost.html', error = error, 
                                        subject = subject, 
                                        content = content)

class SignUpHandler(main_handler.Handler):
    def get(self):
        self.render('signup.html')

    def post(self):
        username = self.get_from_request('username')
        password = self.get_from_request('password')
        verify = self.get_from_request('verify')
        email = self.get_from_request('email')

        params, error = user_stuff.valid_signup_form(username,password, 
                                                     verify,email)
        
        if error:
            self.render('signup.html', **params)       
        else:
            user_id = model.new_user(username, password, email)
            self.set_user_cookie(user_id)
            self.redirect('/welcome')

class WelcomeHandler(main_handler.Handler):
    def get(self):
        if self.user:
            user_id = self.user.user_id()
            username = model.user_by_id(user_id).username
            self.render('welcome.html', username = username)
        else:
            self.redirect('/login')

class LoginHandler(main_handler.Handler):
    def get(self):
        # when a not logged user goes to /newpost he 
        # is redirect to /login?from_path=/newpost
        from_newpost = self.get_from_request('from_path')
        self.render('login.html', from_newpost = from_newpost)

    def post(self):
        username = self.get_from_request('username')
        password = self.get_from_request('password')
        from_path = self.get_from_request('from_path')
        user = model.user_by_name(username)
        if user:
            if user_stuff.valid_pw(username, password, user.password):
                self.set_user_cookie(user.user_id())
                path = str(from_path) or '/welcome'
                self.redirect(path)
            else:
                login_error = "Username and Password didn't match"
                self.render('login.html', username = username, 
                                          login_error = login_error)
        else:
            self.render('login.html', login_error = 'Invalid Login')

class LogoutHandler(main_handler.Handler):
    def get(self):
        self.set_cookie('user=; Path=/')
        self.redirect('/')

class IndexJson(main_handler.Handler):
    def get(self):
        posts = model.list_posts()
        self.set_json()
        self.render_json([p.as_dict() for p in posts])

class PermaLinkJson(main_handler.Handler):
    def get(self, post_id):
        post = model.post_by_id(post_id)
        self.set_json()
        if post:
            self.render_json(post.as_dict())

import webapp2
app = webapp2.WSGIApplication([('/', Index),
                               ('/newpost', NewPost),
                               ('/posts/([0-9]+)', PermaLink),
                               ('/signup', SignUpHandler),
                               ('/welcome', WelcomeHandler),
                               ('/login', LoginHandler),
                               ('/logout', LogoutHandler),
                               ('/?.json', IndexJson),
                               ('/posts/([0-9]+)/?.json', PermaLinkJson)
                                ],
                                debug=False)