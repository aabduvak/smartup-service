from rest_framework import serializers

from django.contrib.auth import get_user_model

User = get_user_model()

class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(source="key")
    key = serializers.CharField(write_only=True)

class AuthSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            try:
                user = User.objects.get(**{"email__iexact": email})
            except User.DoesNotExist:
                user = None

            if user:
                if not user.is_active:
                    msg = "User account is disabled."
                    raise serializers.ValidationError(msg)
                if not user.check_password(password):
                    msg = "Invalid email or password."
                    raise serializers.ValidationError(msg)
            else:
                msg = "No account is associated with this alias."
                raise serializers.ValidationError(msg)
        else:
            msg = "Missing email or password"
            raise serializers.ValidationError(msg)

        attrs["user"] = user
        return attrs