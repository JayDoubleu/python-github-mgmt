import re
import requests
from bs4 import BeautifulSoup


def rotate_github_password(username, password, new_password):
    try:
        url = 'https://github.com'
        s = requests.Session()
        response = s.get(
            url +
            '/login?return_to=https%3A%2F%2Fgithub.com%2Fsettings%2Fadmin'
        ).content
        soup = BeautifulSoup(response, features='html.parser')
        token = soup.find('input', {'name': 'authenticity_token'}).get('value')
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
            'login': username,
            'password': password
        }
        login_response = s.post(url + '/session', data=data).content

        soup = BeautifulSoup(login_response, features='html.parser')
        pwd_form = soup.find('form', {'class': 'edit_user'})
        token = pwd_form.find('input', {
            'name': 'authenticity_token'
        }).get('value')

        data = {
            'utf8': '✓',
            '_method': 'put',
            'authenticity_token': token,
            'session_revoked': 'false',
            'user[old_password]': password,
            'user[password]': new_password,
            'user[password_confirmation]': new_password
        }
        change_pwd_response = s.post(url + '/account', data=data).content
        soup = BeautifulSoup(change_pwd_response, features='html.parser')
    except:
        pass

    try:
        soup = BeautifulSoup(change_pwd_response, features='html.parser')
    except NameError:
        raise Exception('Failed to change password - Possibly wrong password')

    try:
        if not re.search('Password changed successfully', soup.getText()):
            raise Exception('Failed to change password - Unknown error')

    except Exception as e:
        raise Exception(e)


rotate = rotate_github_password('username', 'old_pwd', 'new_pwd')
