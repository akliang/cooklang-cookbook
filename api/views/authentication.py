from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class LoginTokenAuth(ObtainAuthToken):
  # TODO: create user folder on create
  # TODO: enable logging

  def post(self, request, *args, **kwargs):
    serializer = self.serializer_class(data=request.data,
                                        context={'request': request})
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    token, created = Token.objects.get_or_create(user=user)
    return Response({
        'token': token.key,
        # 'username': user.username,
    })

  
def lookup_user_by_api(api_key):
  token = Token.objects.get(key=api_key)
  return token.user