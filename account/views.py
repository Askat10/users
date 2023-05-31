from rest_framework.generics import CreateAPIView, DestroyAPIView
from .serializers import RegistrationSerializer, ActivationSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_202_ACCEPTED, HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy



class RegistrationView(CreateAPIView):
    serializer_class = RegistrationSerializer

class ActivationView(CreateAPIView):
    serializer_class = ActivationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.activate()
        return Response({'message': 'Account activated successfully'}, status=HTTP_202_ACCEPTED)
    

class LoginView(ObtainAuthToken):
    serializer_class=LoginSerializer

class LogoutView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request: Request):
        print(request.user.username)
        Token.objects.get(user=request.user).delete()
        return Response({'message': 'Logged out'}, status=HTTP_204_NO_CONTENT)
    
class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    success_url = reverse_lazy('success')

    def form_valid(self, form):
        user = self.request.user
        old_password = form.cleaned_data.get('old_password')
        new_password = form.cleaned_data.get('new_password1')

        if authenticate(username=user.username, password=old_password):
            user.set_password(new_password)
            user.save()
         
            return super().form_valid(form)
        else:
            form.add_error('old_password', 'Неверный текущий пароль')
            return self.form_invalid(form)


    
