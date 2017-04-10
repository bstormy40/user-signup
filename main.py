import webapp2
import re
import cgi

signup_form = """"
<!DOCTYPE html>
<html>
    <head>
        <style>
            .error {
                color: red;
            }
        </style>
    </head>
    <body>
    <h1>Signup</h1>
        <form method="post">
            <table>
                <tr>
                    <td><label for="username">Username</label></td>
                    <td>
                        <input name="username" type="text" value="" required>
                        <span class="error"></span>
                    </td>
                </tr>
                <tr>
                    <td><label for="password">Password</label></td>
                    <td>
                        <input name="password" type="password" required>
                        <span class="error"></span>
                    </td>
                </tr>
                <tr>
                    <td><label for="verify">Verify Password</label></td>
                    <td>
                        <input name="verify" type="password" required>
                        <span class="error"></span>
                    </td>
                </tr>
                <tr>
                    <td><label for="email">Email (optional)</label></td>
                    <td>
                        <input name="email" type="email" value="">
                        <span class="error"></span>
                    </td>
                </tr>
            </table>
            <input type="submit">
        </form>
    </body>
</html>"""

welcome_form = """<!DOCTYPE html>
<html>
	<head>
		<title>Unit 2 Signup - Welcome</title>
	</head>
	<body>
		<h2>Welcome, %s!</h2>
	</body>
</html>
"""

def escape_html(s):
	return cgi.escape(s, quote = True)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(s):
    return USER_RE.match(s)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(s):
    return PASS_RE.match(s)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(s):
    if s == "":
        return True
    else:
        return EMAIL_RE.match(s)


class Signup(webapp2.RequestHandler):
    def write_form(self, username="", email="", e_name="", e_pass="", e_verify="", e_email=""):
		self.response.out.write(signup_form % {"username": escape_html(username), "email": escape_html(email), "e_name": e_name, "e_pass": e_pass, "e_verify": e_verify, "e_email": e_email})

    def get(self):
        self.write_form()

    def post(self):
		user_name = self.request.get('username')
		user_pass = self.request.get('password')
		user_verify = self.request.get('verify')
		user_email = self.request.get('email')

		name = valid_name(user_name)
		password = valid_pass(user_pass)
		verify = valid_pass(user_verify)
		email = valid_email(user_email)

		e_name = ''
		e_pass = ''
		e_verify = ''
		e_email = ''

		if not name:
			e_name = 'That is not a valid name'
		if not password:
			e_pass = 'That is not a valid password'
		if not match_pass(user_pass, user_verify):
			e_verify = 'The two passwords do not match'
		if not email:
			e_email = 'That is not a valid email'

		if password and (not e_verify) and name and email:
			self.redirect('/welcome?username=%s' % user_name)
		else:
			self.write_form(user_name, user_email, e_name, e_pass, e_verify, e_email)

class WelcomeHandler(webapp2.RequestHandler):
	def get(self):
		username = self.request.get('username')
		self.response.out.write(welcome_form % username)

app = webapp2.WSGIApplication([
    ('/', Signup)
    ('/welcome', WelcomeHandler)
], debug=True)
