from typing import Any, Dict
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class ObtainTokenSerializer(TokenObtainPairSerializer):
    def validate_email(self, email: str):
        email_prefix, email_suffix = email.split('@')
        email_prefix = email_prefix.replace('.', '')
        email = f"{email_prefix}@{email_suffix}"
        return email
    
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        attrs['username'] = attrs['email']
        attrs = super().validate(attrs)
        return attrs
