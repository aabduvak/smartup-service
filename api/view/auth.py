from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny

from api.serializer.user import TokenSerializer, AuthSerializer


class AuthView(APIView):
    permission_classes = [
        AllowAny,
    ]
    serializer_class = AuthSerializer

    def post(self, request):

        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data["user"]

            (token, _) = Token.objects.get_or_create(user=user)

            if token:
                token_serializer = TokenSerializer(data=token.__dict__, partial=True)
                if token_serializer.is_valid():
                    # Return our key for consumption.
                    return Response(
                        data={"token": token_serializer.data["token"]},
                        status=200,
                    )
        return Response(serializer.error_messages, status=200)
