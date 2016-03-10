import hashlib
import random
import string
import hmac
import re
from secret import secret
import model

#Signup stuff
def valid_username(username):
    return username and re.match('^[\S]+$', username)

def valid_password(password, verify):
    return password and password == verify

def valid_email(email):
    return not email or re.match('^[\S]+@[\S]+\.[\S]+$', email)

#Password stuff
def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))

def make_pw_hash(name, pw, salt = None):
    if not salt:
        salt = make_salt() 
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (h, salt)

def valid_pw(name, pw, h):
    salt = h.split(',')[1]
    return h == make_pw_hash(name, pw, salt)

#Cookies stuff
def hash_str(s):
    return hmac.new(secret, s, hashlib.sha256).hexdigest()

def make_secure_val(s):
    return '%s|%s' % (s, hash_str(s))

def check_secure_val(h):
    val = h.split('|')[0]
    if h == make_secure_val(val):
        return val

#Form stuff
def valid_signup_form(username, password, verify, email):
    have_error = False
    params = {'username_value': username,
              'email_value': email}

    if model.user_by_name(username):
        have_error = True
        params['username_error'] = "That username is not available."
    if not valid_username(username):
        have_error = True
        params['username_error'] = "That's not a valid username."
    if not password:
        have_error = True
        params['password_error'] = "That's not a valid password."   
    elif not valid_password(password, verify):
        have_error = True
        params['verify_error'] = "Sorry, the passwords didn't match."
    if not valid_email(email):
        have_error = True
        params['email_error'] = "That's not a valid e-mail."

    return params, have_error
