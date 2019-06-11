import re
import json
import sys
import time
import requests
import pyotp
from bs4 import BeautifulSoup


class Github_mgmt(object):
    def __init__(self, **kwargs):
        self.url = 'https://github.com'
        self.api_url = 'https://api.github.com'
        self.github_username = kwargs['github_username']
        self.github_password = kwargs['github_password']
        self.github_otp_secret = kwargs['github_otp_secret']

    def get_otp(self, secret):
        return pyotp.TOTP(secret).now()

    def get_authorizations(self):
        try:
            s = requests.Session()
            s.auth = (self.github_username, self.github_password)
            headers = {
                'X-GitHub-OTP': self.get_otp(self.github_otp_secret),
                'Content-type': 'application/json',
                'Accept': 'application/vnd.github.v3+json'
            }
            s.headers.update(headers)

            return s.get(self.api_url + '/authorizations').json()

        except Exception as e:
            raise Exception('Unable to retrieve authorizations')

    def get_authorization_by_id(self, authorization_id):
        try:
            s = requests.Session()
            s.auth = (self.github_username, self.github_password)
            headers = {
                'X-GitHub-OTP': self.get_otp(self.github_otp_secret),
                'Content-type': 'application/json',
                'Accept': 'application/vnd.github.v3+json'
            }
            s.headers.update(headers)

            return s.get(self.api_url + '/authorizations/' +
                         str(authorization_id)).json()

        except Exception as e:
            raise Exception('Unable to retrieve authorization id: {0}'.format(
                authorization_id))

    def create_authorization(self, payload):
        try:
            s = requests.Session()
            s.auth = (self.github_username, self.github_password)
            headers = {
                'X-GitHub-OTP': self.get_otp(self.github_otp_secret),
                'Content-type': 'application/json',
                'Accept': 'application/vnd.github.v3+json'
            }
            s.headers.update(headers)

            return s.post(self.api_url + '/authorizations',
                          json=payload).json()

        except Exception as e:
            raise Exception('Unable to create authorization')

    def delete_authorization(self, authorization_id):
        try:
            s = requests.Session()
            s.auth = (self.github_username, self.github_password)
            headers = {
                'X-GitHub-OTP': self.get_otp(self.github_otp_secret),
                'Content-type': 'application/json',
                'Accept': 'application/vnd.github.v3+json'
            }
            s.headers.update(headers)
            s.delete(self.api_url + '/authorizations/' + str(authorization_id))

        except Exception as e:
            raise Exception('Unable to remove authorization id: {0}'.format(
                authorization_id))

    def get_repo_invitations(self):
        try:
            s = requests.Session()
            s.auth = (self.github_username, self.github_password)
            headers = {
                'X-GitHub-OTP': self.get_otp(self.github_otp_secret),
                'Content-type': 'application/json',
                'Accept': 'application/vnd.github.v3+json'
            }
            s.headers.update(headers)

            return s.get(self.api_url + '/user/repository_invitations').json()

        except Exception as e:
            raise Exception('Unable to retrieve user repository invitations')

    def accept_repo_invitation(self, invitation_id):
        try:
            s = requests.Session()
            s.auth = (self.github_username, self.github_password)
            headers = {
                'X-GitHub-OTP': self.get_otp(self.github_otp_secret),
                'Content-type': 'application/json',
                'Accept': 'application/vnd.github.v3+json'
            }
            s.headers.update(headers)

            return s.patch(self.api_url + '/user/repository_invitations/' +
                           str(invitation_id))

        except Exception as e:
            raise Exception(
                'Unable to accept user repository invitation id: '.format(
                    invitation_id))

    def decline_repo_invitation(self, invitation_id):
        try:
            s = requests.Session()
            s.auth = (self.github_username, self.github_password)
            headers = {
                'X-GitHub-OTP': self.get_otp(self.github_otp_secret),
                'Content-type': 'application/json',
                'Accept': 'application/vnd.github.v3+json'
            }
            s.headers.update(headers)

            return s.delete(self.api_url + '/user/repository_invitations/' +
                            str(invitation_id))

        except Exception as e:
            raise Exception(
                'Unable to decline user repository invitation id: '.format(
                    invitation_id))

    def rotate_password(self, new_password):
        try:
            s = requests.Session()
            response = s.get(
                self.url + '/login?' +
                'return_to=https%3A%2F%2Fgithub.com%2Fsettings%2Fadmin'
            ).content
            soup = BeautifulSoup(response, features='html.parser')
            token = soup.find('input', {
                'name': 'authenticity_token'
            }).get('value')
            headers = {
                'Content-type': 'application/x-www-form-urlencoded',
                'Accept': 'text/html',
                'Connection': 'keep-alive'
            }
            s.headers.update(headers)
            data = {
                'commit': 'Sign in',
                'utf8': '✓',
                'authenticity_token': token,
                'login': self.github_username,
                'password': self.github_password
            }
            login_response = s.post(self.url + '/session', data=data).content

            soup = BeautifulSoup(login_response, features='html.parser')
            token = soup.find('input', {
                'name': 'authenticity_token'
            }).get('value')

            data = {
                'utf8': '✓',
                'authenticity_token': token,
                'otp': self.get_otp(self.github_otp_secret)
            }
            otp_response = s.post(self.url + '/sessions/two-factor',
                                  data=data).content

            soup = BeautifulSoup(otp_response, features='html.parser')
            pwd_form = soup.find('form', {'class': 'edit_user'})
            token = pwd_form.find('input', {
                'name': 'authenticity_token'
            }).get('value')

            data = {
                'utf8': '✓',
                '_method': 'put',
                'authenticity_token': token,
                'session_revoked': 'false',
                'user[old_password]': self.github_password,
                'user[password]': new_password,
                'user[password_confirmation]': new_password
            }
            change_pwd_response = s.post(self.url + '/account',
                                         data=data).content
            soup = BeautifulSoup(change_pwd_response, features='html.parser')
        except:
            pass

        try:
            soup = BeautifulSoup(change_pwd_response, features='html.parser')
        except NameError:
            raise Exception(
                'Failed to change password - Possibly wrong password')

        try:
            if not re.search('Password changed successfully', soup.getText()):
                raise Exception('Failed to change password - Unknown error')

        except Exception as e:
            raise Exception(e)
