from google.appengine.ext import db
import user_stuff
import bleach

class Post(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    author = db.StringProperty(required = True)

    def as_dict(self):
        time_fmt = '%c'
        d = {'subject': self.subject,
             'content': self.content,
             'created': self.created.strftime(time_fmt),
             'author': self.author}
        return d

    def post_id(self):
        return self.key().id()

    def escape_content(self):
        self.content = bleach.clean(self.content)
        self.content = self.content.replace('\n', '<br>')
        return bleach.clean(self.content, tags=['br'])

class Users(db.Model):
    username = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    email = db.StringProperty()
    register_date = db.DateTimeProperty(auto_now_add = True)

    def user_id(self):
        return self.key().id()
    

def list_posts():
    posts = db.GqlQuery("select * from Post order by created desc limit 10")
    return list(posts)

def post_by_id(post_id):
    return Post.get_by_id(int(post_id))

def new_post(subject, content, author):
    new = Post(subject = subject, content = content, author = author)
    new.put()
    return new.post_id()


def user_by_name(username):
    return Users.all().filter('username =', username).get()

def user_by_id(user_id):
    if user_id:
        return Users.get_by_id(int(user_id))

def new_user(username, password, email = None):
    password = user_stuff.make_pw_hash(username, password)
    new = Users(username = username,
                password = password,
                email = email)
    new.put()
    return new.user_id()