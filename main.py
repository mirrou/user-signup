import webapp2
import re


# html boilerplate for the top of every page
page_header =
<!DOCTYPE html>
<html>
<head>
    <title>User-Signup</title>
    <style type="text/css">
        .error {
        color: red;
        }
    </style>
</head>
<body>
    <h2>Signup</h2>


# html boilerplate for the bottom of every page
page_footer =
</body>
</html>


class Index (webapp2.RequestHandler):
    #Handles requests coming in to '/' (the root of our site)
    def get(self):
        # a form for adding new movies
        username_form ="""
        <form  method="post">
            <label>
                Username
                <input type="text" name="username"/>
            </label>
        </form>
        """
        password_form ="""
        <form  method="post">
            <label>
                Password
                <input type="password" name="password"/>
            </label>
        </form>
        """
        verify_password_form ="""
        <form  method="post">
            <label>
                Verify Password
                <input type="password" name="verify"/>
            </label>
        </form>
        """
        email_form ="""
        <form  method="post">
            <label>
                Email (optional)
                <input type="text" name="email">
            </label>
        </form>
        """

        # if we have an error, make a <p> to display it
        error = self.request.get("error")
        error_element = "<p class='error'>" + error + "</p>"

        # combine all the pieces to build the content of our response
        main_content = username_form +  password_form + verify_password_form +
        email_form + error_element
        content = page_header + main_content + page_footer
        self.response.write(content)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)



class Signup (webapp2.RequestHandler):
    # Handles requests coming in to '/signup'

    def post(self):
        # look inside the request to figure out what the user typed
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')


        if not valid_username(username):
            error = "That's not a valid username."
            have_error = True
            self.redirect("/?error=" (error))

        if not valid_password(password):
            error = "That wasn't a valid password."
            have_error = True
            self.redirect("/?error=" (error))

        elif password != verify:
            error = "Your passwords didn't match."
            have_error = True
            self.redirect("/?error=" (error))

        if not valid_email(email):
            error = "That's not a valid email."
            have_error = True
            self.redirect("/?error=" (error))

        else:
            self.redirect('/welcome?username=' + username)



class Welcome (webapp2.RequestHandler):
    """ Handles requests coming in to '/welcome'
    """
    def get(self):
        #look inside the request to fine the username
        username = self.request.get('username')

        # build response content
        welcome_message: "Welcome, {0}!".format(username)
        content = page_header + welcome_message + page_footer

        if valid_username(username):
            self.response.write(content)
        else:
            self.redirect('/signup')

app = webapp2.WSGIApplication([
    ('/', Index),
    ('/signup', Signup),
    ('/welcome', Welcome)
], debug=True)
