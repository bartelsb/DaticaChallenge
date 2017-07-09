import falcon
import DatabaseInteractions
import EncryptionFunctions
import os
import json

if os.path.exists(DatabaseInteractions.database_file):
    print(str('Database exists'))
else:
    print(str('Creating database'))
    DatabaseInteractions.create_database()


class BaseResource(object):

    def on_get(self, req, resp):
        session_token = req.get_param('session_token')
        if EncryptionFunctions.authenticate(session_token):
            username = EncryptionFunctions.retrieve_username(session_token)
            user_data = DatabaseInteractions.retrieve_user(username)
            resp.status = falcon.HTTP_200
            # index 4 is additional data
            resp.body = '{username: ' + username + ', additional_info: ' + str(user_data[4]) + '}'
        else:
            resp.status = falcon.HTTP_200
            resp.content_type = 'application/json'
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

    def on_get(self, req, resp, username):
        token = req.get_param('session_token', True)
        if EncryptionFunctions.authenticate(token) and EncryptionFunctions.retrieve_username(token) == username:
            user_data = DatabaseInteractions.retrieve_user(username)
            if not user_data:
                raise falcon.exceptions.HTTPNotFound()
            resp.status = falcon.HTTP_200
            resp.content_type = 'application/json'
            resp.body = '{username: ' + username + ', additional_info: ' + str(user_data[4]) + '}'
        else:
            resp.status = falcon.HTTP_401

    def on_put(self, req, resp, username):
        token = req.get_param('session_token', True)
        if EncryptionFunctions.authenticate(token) and EncryptionFunctions.retrieve_username(token) == username:
            additional_info = req.get_param('additional_info')
            DatabaseInteractions.update_user(username, additional_info)
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_401

    def on_delete(self, req, resp, username):
        token = req.get_param('session_token', True)
        if EncryptionFunctions.authenticate(token) and EncryptionFunctions.retrieve_username(token) == username:
            # May want to consider deleting session token here as well, unless implementing admin roles
            DatabaseInteractions.delete_user(username)
            resp.status = falcon.HTTP_204
        else:
            resp.status = falcon.HTTP_401


class AuthenticationResource(object):

    def on_post(self, req, resp):
        username = req.get_param('username', True)
        password = req.get_param('password', True)
        retrieved_user = DatabaseInteractions.retrieve_user(username)
        if retrieved_user is None:
            resp.status = falcon.HTTP_401
            return
        if not EncryptionFunctions.check_password(password, retrieved_user[2], retrieved_user[3]):  # index 2 is password, index 3 is salt for hash
            resp.status = falcon.HTTP_401
            return
        session_token = EncryptionFunctions.generate_session_token(username)
        resp.status = falcon.HTTP_200
        resp.content_type = 'application/json'
        resp.body = '{session_token: ' + session_token + '}'

    def on_delete(self, req, resp):
        token = req.get_param('session_token', True)
        if EncryptionFunctions.authenticate(token):
            EncryptionFunctions.delete_session_token(token)
            resp.status = falcon.HTTP_204
        else:
            resp.status = falcon.HTTP_401


app = falcon.API()

default = BaseResource()
user = UserResource()
auth = AuthenticationResource()

app.add_route('/', default)
app.add_route('/user', user)
app.add_route('/user/{username}', user)
app.add_route('/auth', auth)

app.req_options.auto_parse_form_urlencoded = True  # allows form content to be included as query string params
