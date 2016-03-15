import hashlib
import random
import string
import hmac
import re
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

#Very simple cache to avoid login just copying the cookies
session_cache = {}
def set_token(user):
    token = session_cache[str(user)] = make_salt()
    return token

def get_token(user):
    try:
        return session_cache[str(user)]
    except:
        return ' ' # Must not return None or hmac will not work properly

def delete_token(user):
    try:
        del session_cache[str(user)]
        return True
    except:
        return False

#Cookies stuff
def hash_str(s, token = None):
    if not token:
        token = set_token(s)
        return hmac.new(token, s, hashlib.sha256).hexdigest()
    return hmac.new(token, s, hashlib.sha256).hexdigest()

def make_secure_val(s, token = None):
    return '%s|%s' % (s, hash_str(s, token))

def check_secure_val(h):
    val = h.split('|')[0]
    token = get_token(val)
    if h == make_secure_val(val, token):
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
