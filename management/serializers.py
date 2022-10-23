from rest_framework import serializers

from .models import Account

class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['name', 'nmec', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        account = Account(
                name=self.validated_data['name'],
                nmec=self.validated_data['nmec'],
                username=self.validated_data['username'],
                is_admin=True,
                is_active=True,
                is_staff=True
            )
        password = self.validated_data['password']

        account.set_password(password)
        account.save()
        return account