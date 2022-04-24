from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.authentication import get_authorization_header
from api.forms import ChefCreationForm
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.forms import PasswordChangeForm


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
    if form.is_valid():
      form.save()
      return Response(f"User {request.POST['username']} has been registered.")
    else:
      return Response(form.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DeleteAccount(APIView):
  def post(self, request, *args, **kw):
    user = lookup_user_by_api(request)
    if user:
      user.delete()
      return JsonResponse({'username': user.username})
    else:
      return Response("User account not found.")

class ChangeAccountPassword(APIView):
  def post(self, request, *args, **kw):
    user = lookup_user_by_api(request)
    if user:
      form = PasswordChangeForm(user, request.POST)
      if form.is_valid():
        form.save()
        # delete the API token to force a new key on next login
        Token.objects.get(user=user).delete()
        return Response("Password updated.")
      else:
        return Response(form.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
      return Response("Something went wrong - password not changed.")

  
# helper function to convert API key into username
def lookup_user_by_api(request):
  auth = get_authorization_header(request).split()
  if auth[1].decode() != 'undefined':
    api_key = auth[1].decode()
    token = Token.objects.get(key=api_key)
    return token.user
  else:
    return None