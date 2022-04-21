from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authentication import get_authorization_header
from django.contrib.auth.models import User
from django.views import View
from api.forms import ChefCreationForm
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework import status


class LoginTokenAuth(ObtainAuthToken):
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


@method_decorator(csrf_exempt, name='dispatch')
class RegisterAccount(APIView):
  def post(self, request, *args, **kw):
    form = ChefCreationForm(request.POST)
    print(request.POST)
    print(form.is_valid())
    if form.is_valid():
      form.save()
      # TODO: create folder/account?
      return Response(f"User {request.POST['username']} has been registered.")
    else:
      return Response(form.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

  
# helper function to convert API key into username
def lookup_user_by_api(request):
  auth = get_authorization_header(request).split()
  if auth:
    api_key = auth[1].decode()
    token = Token.objects.get(key=api_key)
    return token.user
  else:
    return None