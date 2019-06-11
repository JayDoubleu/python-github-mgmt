# python-github-mgmt
Python script to manage github account

```python
from github_mgmt import Github_mgmt
gmgmt = Github_mgmt(github_username='username',
                    github_password='password',
                    github_otp_secret='otp_secret')
```

```python
authorizations = gmgmt.get_authorizations()
```

```python
for authorization in authorizations:
    gmgmt.delete_authorization(authorization['id'])
```

https://developer.github.com/apps/building-oauth-apps/understanding-scopes-for-oauth-apps/
https://developer.github.com/v3/oauth_authorizations/#create-a-new-authorization

```python
data = {"scopes": ["repo"], "note": "admin script"}
authorization = gmgmt.create_authorization(data)
oauth_token = authorization['token']
```

```python
invitations = gmgmt.get_repo_invitations()
```

```python
for invitation in gmgmt.get_repo_invitations():
    gmgmt.accept_repo_invitation(invitation['id'])
```
```python
for invitation in gmgmt.get_repo_invitations():
    gmgmt.decline_repo_invitation(invitation['id'])
```


```python
gmgmt.rotate_password('new_password')
```
