import os
import jinja2
import webapp2
import json
import user_stuff

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), 
                               autoescape=True)

class Handler(webapp2.RequestHandler):
    def render(self, template, **params):
        t = jinja_env.get_template(template)
        self.response.write(t.render(params))

    def get_from_request(self, var):
        return self.request.get('%s' % var)

    def set_cookie(self, cookie):
        self.response.headers.add_header('Set-Cookie', '%s' % cookie)

    def set_user_cookie(self, user):
        user_cookie = str(user_stuff.make_secure_val(str(user)))
        self.set_cookie('user=%s; Path=/' % user_cookie)

    def get_cookie(self, cookie_name):
        return self.request.cookies.get('%s' % cookie_name)

    def set_json(self):
        self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'

    def render_json(self, py_dict):
        json_txt = json.dumps(py_dict)
        self.response.write(json_txt)

    def is_logged(self):
        user = self.get_cookie('user')
        if user:
            return user_stuff.check_secure_val(user)