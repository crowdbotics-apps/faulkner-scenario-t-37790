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


class AppViewSet(ModelViewSet):
    serializer_class = AppSerializer
    http_method_names = ["get", "post", "put", "patch", "delete"]
    queryset = App.objects.all()

    # def list(self, request):
    #     objects = App.objects.all()
    #     serializer = self.serializer_class(objects, many=True)
    #     return Response(serializer.data)

    # def create(self, request):
    #     pass

    # def retrieve(self, request, pk=None):
    #     pass

    # def update(self, request, pk=None):
    #     pass

    # def partial_update(self, request, pk=None):
    #     pass

    # def destroy(self, request, pk=None):
    #     pass 


class PlanViewSet(ModelViewSet):
    serializer_class = PlanSerializer
    http_method_names = ["get"]
    queryset = Plan.objects.all()

    # def list(self, request):
    #     pass

    # def retrieve(self, request, pk=None):
    #     pass


class SubscriptionViewSet(ModelViewSet):
    serializer_class = SubscriptionSerializer
    http_method_names = ["get", "post", "put", "patch"]
    queryset = Subscription.objects.all()

    # def list(self, request):
    #     pass

    # def create(self, request):
    #     pass

    # def retrieve(self, request, pk=None):
    #     pass

    # def update(self, request, pk=None):
    #     pass

    # def partial_update(self, request, pk=None):
    #     pass
