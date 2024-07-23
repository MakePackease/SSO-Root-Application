from rest_framework_simplejwt.tokens import AccessToken

class CustomAccessToken(AccessToken):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self['sub'] = self.get('user_id')
