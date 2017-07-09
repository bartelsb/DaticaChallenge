import falcon
import DatabaseInteractions
import EncryptionFunctions
import os


class BaseResource(object):

    def on_get(self, req, resp):
        session_token = req.get_param('session_token')
        # authenticate if possible
        username = 'username'
        additional_info = '{phone_number:(123)456-7890}'
        authenticated = False
        if authenticated:
            DatabaseInteractions.retrieve_user(username)
            resp.status = falcon.HTTP_200
            resp.body = '{username: ' + username + ', additional_info: ' + additional_info + '}'
        else:
            resp.status = falcon.HTTP_200
            resp.body = '{response: "Hello World"}'


class UserResource(object):

    def on_post(self, req, resp):
        username = req.get_param('username', True)
        password = req.get_param('password', True)
        additional_info = req.get_param('additional_info')
        is_admin = req.get_param_as_bool('is_admin')
        password_object = EncryptionFunctions.encrypt_password(password)
        enc_password = password_object[0]
        salt = password_object[1]
        DatabaseInteractions.create_user(username, enc_password, salt, additional_info, is_admin)
        resp.status = falcon.HTTP_200

    def on_get(self, req, resp):
        # authenticate
        username = 'username'
        resp.status = falcon.HTTP_200
        resp.body = DatabaseInteractions.retrieve_user(username)


    def on_put(self, req, resp):
        # authenticate
        for param in req.get_params():
            if param(0) == 'username':
                username = param(1)
            if param(0)=='password':
                password = param(1)

        username = 'username'
        additional_info = '{additional: info}'
        resp.status = falcon.HTTP_200
        DatabaseInteractions.update_user(username, additional_info)

    def on_delete(self, req, resp):
        # authenticate
        username = 'username'
        DatabaseInteractions.delete_user(username)
        resp.status = falcon.HTTP_200
        # if not authenticated, return unauthorized


class AuthenticationResource(object):

    def on_post(self, req, resp):
        resp.status = falcon.HTTP_200

    def on_delete(self, req, resp):
        # authenticate
        resp.status = falcon.HTTP_200

    def authenticate(self, username, password):
        # query on username, compare password using encryption
        return 0


app = falcon.API()

default = BaseResource()
user = UserResource()
auth = AuthenticationResource()

app.add_route('/', default)
app.add_route('/user', user)
app.add_route('/auth', auth)

if os.path.exists(DatabaseInteractions.database_file):
    str("Database exists")
else:
    DatabaseInteractions.create_database()
