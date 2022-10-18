from rest_framework import serializers

from .models import Account

class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        account = Account(
                username=self.validated_data['username'],
                is_admin=True,
                is_active=True,
                is_staff=True
            )
        password = self.validated_data['password']

        account.set_password(password)
        account.save()
        return account