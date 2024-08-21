ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_CONFIRMATION_URL = 'http://127.0.0.1:3000/confirmation'
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = 'http://127.0.0.1:3000/confirmation'
GOOGLE_LOGIN_REDIRECT_URL = 'http://127.0.0.1:3000/'
GOOGLE_TOKEN_URL = 'https://oauth2.googleapis.com/token'
GOOGLE_USERINFO_URL = 'https://www.googleapis.com/oauth2/v3/userinfo'

GOOGLE_CREDENTIALS = {
    "test":{
        "client_id" : None,
        "secret": None
    }
}

SITE_NAME = 'VidasanBackend'
FRONTEND_URL = 'http://localhost:3000/'
RESET_PASSWORD_REDIRECT_PATH = 'reset-password/'