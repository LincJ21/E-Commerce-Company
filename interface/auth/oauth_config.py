from authlib.integrations.starlette_client import OAuth
from interface.auth.sso_authentication import CLIENT_ID, CLIENT_SECRET

oauth = OAuth()
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    client_kwargs={
        'scope': 'email openid profile',
        'redirect_uri': 'https://e-commerce-company-9lgu.onrender.com/auth',
        'prompt':'login'}
    )