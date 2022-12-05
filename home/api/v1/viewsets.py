from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from home.models import App, Plan, Subscription

from home.api.v1.serializers import (
    SignupSerializer,
    UserSerializer,
    AppSerializer,
    PlanSerializer,
    SubscriptionSerializer,
)


class SignupViewSet(ModelViewSet):
    serializer_class = SignupSerializer
    http_method_names = ["post"]


class LoginViewSet(ViewSet):
    """Based on rest_framework.authtoken.views.ObtainAuthToken"""

    serializer_class = AuthTokenSerializer

    def create(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        user_serializer = UserSerializer(user)
        return Response({"token": token.key, "user": user_serializer.data})

class PrimaryKeyException(Exception):
    pass 

class UserAuthException(Exception):
    pass

class AppViewSet(ModelViewSet):
    serializer_class = AppSerializer
    http_method_names = ["get", "post", "put", "patch", "delete"]
    queryset = App.objects.all()

    def retrieve(self, request, pk=None):
        if pk == None:
            raise PrimaryKeyException('Primary key is required for single App GET.')

        requested_app = App.objects.get(id=pk)
        if request.user == requested_app.user:
            return super().retrieve(request, pk)
        raise UserAuthException('Request User does not own app.')

    def update(self, request, pk=None):
        if pk == None:
            raise PrimaryKeyException('Primary key is required for App POST.')

        requested_app = App.objects.get(id=pk)
        if request.user == requested_app.user:
            return super().update(request, pk)
        raise UserAuthException('Request User does not own app.')

    def partial_update(self, request, pk=None):
        if pk == None:
            raise PrimaryKeyException('Primary key is required for App POST.')

        requested_app = App.objects.get(id=pk)
        if request.user == requested_app.user:
            return super().partial_update(request, pk)
        raise UserAuthException('Request User does not own app.')

    def destroy(self, request, pk=None):
        if pk == None:
            raise PrimaryKeyException('Primary key is required for App POST.')

        requested_app = App.objects.get(id=pk)
        if request.user == requested_app.user:
            return super().destroy(request, pk)
        raise UserAuthException('Request User does not own app.') 


class PlanViewSet(ModelViewSet):
    serializer_class = PlanSerializer
    http_method_names = ["get"]
    queryset = Plan.objects.all()


class SubscriptionViewSet(ModelViewSet):
    serializer_class = SubscriptionSerializer
    http_method_names = ["get", "post", "put", "patch"]
    queryset = Subscription.objects.all()

    def update(self, request, pk=None):
        if pk == None:
            raise PrimaryKeyException('Primary key is required for App POST.')

        requested_app = App.objects.get(id=pk)
        if request.user == requested_app.user:
            return super().update(request, pk)
        raise UserAuthException('Request User does not own app.')

    def partial_update(self, request, pk=None):
        if pk == None:
            raise PrimaryKeyException('Primary key is required for App POST.')

        requested_app = App.objects.get(id=pk)
        if request.user == requested_app.user:
            return super().partial_update(request, pk)
        raise UserAuthException('Request User does not own app.')
