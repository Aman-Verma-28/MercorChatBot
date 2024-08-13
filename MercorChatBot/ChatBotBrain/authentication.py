from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings


class MercorAPIKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        api_key = request.headers.get('mercor_api_key')
        import pdb
        pdb.set_trace()
        if not api_key:
            raise AuthenticationFailed('API Key is required')

        if api_key != settings.MERCOR_API_KEY:
            raise AuthenticationFailed('Invalid API Key')

        return None, None
