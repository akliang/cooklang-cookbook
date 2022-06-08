from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError

from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authentication import get_authorization_header
from rest_framework.views import APIView

from api.forms import ChefCreationForm
from api.models import Chef_Settings

import logging
logger = logging.getLogger(__name__)


class LoginTokenAuth(ObtainAuthToken):
  def post(self, request, *args, **kwargs):
    serializer = self.serializer_class(data=request.data,
                                       context={'request': request})
    # serializer.is_valid(raise_exception=True)
    if serializer.is_valid():
      user = serializer.validated_data['user']
      token, created = Token.objects.get_or_create(user=user)
      if created:
        logger.info(f"{self.__class__.__name__} - API token created for username {user.username}")

      return Response({'token': token.key})
    else:
      logger.warning(f"{self.__class__.__name__} - Failed login attempt for username {request.data['username']} - reason was {serializer.errors}")
      return Response(status=status.HTTP_401_UNAUTHORIZED)


@method_decorator(csrf_exempt, name='dispatch')
class RegisterAccount(APIView):
  def post(self, request, *args, **kw):
    form = ChefCreationForm(request.POST)
    if form.is_valid():
      form.save()
      logger.info(f"{self.__class__.__name__} - New account registered for username {request.POST['username']}")
      return Response(f"User {request.POST['username']} has been registered.")
    else:
      return Response(form.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteAccount(APIView):
  def post(self, request, *args, **kw):
    user = lookup_user_by_api(request)
    if user:
      user.delete()
      logger.info(f"{self.__class__.__name__} - Account deleted for username {user.username}")
      return JsonResponse({'username': user.username})
    else:
      apikey = parse_apikey_from_header(request)
      logger.warning(f"{self.__class__.__name__} - Attempted account deletion failed for API key {apikey}")
      return Response("User account not found.", status=status.HTTP_403_FORBIDDEN)


class ChangeAccountPassword(APIView):
  def post(self, request, *args, **kw):
    user = lookup_user_by_api(request)
    if user:
      form = PasswordChangeForm(user, request.POST)
      if form.is_valid():
        form.save()
        # delete the API token to force a new key on next login
        Token.objects.get(user=user).delete()
        logger.info(f"{self.__class__.__name__} - Password successfully changed for username {user.username}")
        return Response("Password updated.")
      else:
        return Response(form.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
      apikey = parse_apikey_from_header(request)
      logger.warning(f"{self.__class__.__name__} - Invalid password reset attempt using API key {apikey}")
      return Response("Something went wrong - password not changed.", status=status.HTTP_403_FORBIDDEN)

class RequestResetPassword(APIView):
  def post(self, request, *args, **kw):
    form = PasswordResetForm(request.POST)
    if form.is_valid():
      email = form.cleaned_data['email']
      users = User.objects.filter(email=email)
      if users.exists():
        for user in users:
          subject = "Password reset requested"
          email_template_name = "api/password_reset_email.txt"
          c = {
            "email": user.email,
            "domain": settings.FRONTEND_URL,
            "endpoint": "resetpw",
            "site_name": "Cookbook",
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "user": user,
            "token": default_token_generator.make_token(user),
          }
          email = render_to_string(email_template_name, c)
          try:
            send_mail(subject, email, settings.ADMIN_EMAIL, [user.email], fail_silently=False)
            logger.info(f"{self.__class__.__name__} - Password reset requested for {user.username}")
            return Response(True)
          except BadHeaderError:
            return Response("Invalid header", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
      else:
        logger.warning(f"{self.__class__.__name__} - Invalid password reset requested for email {email}")
        return Response("User not found.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
      logger.warning(f"{self.__class__.__name__} - Invalid password reset requested for email {request.POST['email']}")
      return Response("Invalid email.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ResetPassword(APIView):
  def post(self, request, *args, **kw):
    # decode the user
    pk = urlsafe_base64_decode(request.POST['user'])
    user = User.objects.get(pk=pk)

    # check that the token matches the user
    if default_token_generator.check_token(user, request.POST['token']):
      form = SetPasswordForm(user, request.POST)
      if form.is_valid():
        form.save()
        logger.info(f"{self.__class__.__name__} - Password reset changed for {user.username}")
        return Response("Password changed.")
      else:
        return Response(form.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
      logger.warning(f"{self.__class__.__name__} - Invalid user/token combination for password reset (user: {request.POST['user']}, token: {request.POST['token']})")
      return JsonResponse({"msg": ["Invalid token - user not found."]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class Settings(APIView):
  def post(self, request, *args, **kw):
    user = lookup_user_by_api(request)
    if user:
      # if value is supplied, then we are trying to write in a new value
      if 'value' in kw:
        try:
          obj = Chef_Settings.objects.get(chef=user)
          setattr(obj, 'browsable_recipes', kw['value'])
          obj.save()
        except Chef_Settings.DoesNotExist:
          obj = Chef_Settings(chef=user, browsable_recipes=kw['value'])
          obj.save()
        return Response(True)
      # we are polling what the stored value is
      else:
        try:
          obj = Chef_Settings.objects.get(chef=user)
          if obj.browsable_recipes:
            return Response(True)
          else:
            return Response(False)
        except:
          return Response(False)
    else:
      apikey = parse_apikey_from_header(request)
      logger.warning(f"{self.__class__.__name__} - Invalid settings attempt using API key {apikey}")
      return Response("Something went wrong - settings not saved.", status=status.HTTP_403_FORBIDDEN)
  
# helper function to grab the API key from the header
def parse_apikey_from_header(request):
  auth = get_authorization_header(request).split()
  apikey = auth[1].decode()
  if apikey == 'undefined' or apikey == 'null':
    return None
  else:
    return apikey

# helper function to translate the apikey into a User object
def lookup_user_by_api(request):
  apikey = parse_apikey_from_header(request)
  if apikey:
    token = Token.objects.get(key=apikey)
    return token.user
  else:
    return None