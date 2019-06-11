# python-github-mgmt
Python script to manage github account

```python
from github_mgmt import Github_mgmt
gmgmt = Github_mgmt(github_username='username',
                    github_password='password',
                    github_otp_secret='otp_token')
```

```python
authorizations = gmgmt.get_authorizations()
```

```python
for authorization in authorizations:
    gmgmt.delete_authorization(authorization['id'])
```

```python
data = {"scopes": ["repo"], "note": "admin script"}
gmgmt.create_authorization(data)
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
