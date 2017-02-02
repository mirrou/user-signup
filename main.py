import webapp2
import re

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>User-Signup</title>
    <style type="text/css">
        .error {color: red;}
    </style>
</head>
<body>
"""
title = """
<h1>Signup</h1>
"""
# html boilerplate for the bottom of every page
page_footer ="""
</body>
</html>
"""

page_main = """
<form action="/signup" method="post">
  <table>
    <tr>
      <td class="label">
        Username
      </td>
      <td>
        <input type="text" name="username" value="{0}">
      </td>
      <td class="error">
        {2}
      </td>
    </tr>

    <tr>
      <td class="label">
        Password
      </td>
      <td>
        <input type="password" name="password" value="">
      </td>
      <td class="error">
        {3}
      </td>
    </tr>

    <tr>
      <td class="label">
        Verify Password
      </td>
      <td>
        <input type="password" name="verify" value="">
      </td>
      <td class="error">
        {4}
      </td>
    </tr>

    <tr>
      <td class="label">
        Email (optional)
      </td>
      <td>
        <input type="text" name="email" value="{1}">
      </td>
      <td class="error">
        {5}
      </td>
    </tr>
  </table>

  <input type="submit"/>
</form>
"""

class Index(webapp2.RequestHandler):
    def get(self):
        signup = """
        <form action = "/signup" method="post">

            <label>
                Username
                <input type="text" name="username"/>
            </label>

            <br>

            <label>
                Password
                <input type="password" name="password"/>
            </label>

            <br>

            <label>
                Verify Password
                <input type="password" name="verify"/>
            </label>

            <br>

            <label>
                Email (optional)
                <input type="text" name="email">
            </label>

            <br>

            <input type="submit"/>

        </form>
        """


        #combine all the pieces to build the content of our response
        content = page_header + title + signup + page_footer
        self.response.write(content)

class Signup(webapp2.RequestHandler):
    def post(self):
        have_error = False
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        error_element = ""

        if not valid_username(username):
            error_element = error_element + "&error_username= That is not a valid username."
            have_error = True

        if not valid_password(password):
            error_element = error_element + "&error_password= That is not a valid password."
            have_error=True

        elif password != verify:
            error_element = error_element + "&error_verify= Your passwords did not match."
            have_error=True

        if not valid_email(email):
            error_element = error_element + "&error_email= That is not a valid email."
            have_error=True

        if have_error:
            self.redirect('/errors?username=' + username + '&email=' + email + error_element)
        else:
            self.redirect('/welcome?username=' + username)

class errors(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")
        email = self.request.get("email")
        error_username = self.request.get("error_username")
        error_password = self.request.get("error_password")
        error_verify = self.request.get("error_verify")
        error_email = self.request.get("error_email")

        error_refresh = page_main.format(username,email,error_username,error_password,error_verify,error_email)
        self.response.write(page_header + error_refresh + page_footer)

class Welcome (webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        welcome_message = (page_header + "Welcome, " + username + "!" + page_footer)
        if valid_username(username):
            self.response.write(welcome_message)
        else:
            self.redirect('/signup')

app = webapp2.WSGIApplication([
    ('/',Index),
    ('/signup', Signup),
    ('/errors', errors),
    ('/welcome', Welcome)], debug=True)
