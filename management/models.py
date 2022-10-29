from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from api.models import Bars

from neectrally.settings import BASE_DIR

from . import logger

class AccountManager(BaseUserManager):

	def create_user(self, username, password=None):
		if not username:
			raise ValueError("Users must have a username")
		user = self.model(username=username)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, username, password):
		user = self.create_user(
			username=username,
			password=password
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)

		# save superuser token to secrets.py file
		token = Token.objects.get(user=user).key

		return user

class DBLogger(models.Model):
	time = models.CharField(max_length=60)
	message = models.CharField(max_length=500)
	user = models.CharField(max_length=100)

class Account(AbstractBaseUser):

	name = models.CharField(max_length=100, blank=True, null=True)
	nmec = models.IntegerField(blank=True, null=True)
	bar = models.ForeignKey(Bars, on_delete=models.CASCADE, blank=True, null=True)
	username = models.CharField(max_length=30, unique=True)
	date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
	last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
	is_admin = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)

	objects = AccountManager()

	USERNAME_FIELD = 'username'

	def __str__(self):
		return self.username

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return True

# Create Token right away for a register
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
	if created:
		token = Token.objects.create(user=instance)

		# create logging file to /static/logs
		open(f"{BASE_DIR}/static/logs/{token.key}.log", "w").close() 

		# write first log
		logger.info(token.key, f"User {instance.username}{f'({instance.name})' if instance.name is not None else ''} created with token {token.key}")