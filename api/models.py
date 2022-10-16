from django.db import models

class Teams(models.Model):
	name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	points = models.IntegerField(default=0)
	timestamp = models.DateTimeField(auto_now=True)

class Members(models.Model):
	name = models.CharField(max_length=255)
	course = models.CharField(max_length=255)
	nmec = models.IntegerField()
	points = models.IntegerField(default=0)
	team = models.ForeignKey(Teams, on_delete=models.CASCADE)

class Admin(models.Model):
	username = models.CharField(max_length=255)
	pwd = models.TextField()
	timestamp = models.DateTimeField(auto_now=True)

class Bars(models.Model):
    name = models.CharField(max_length=255)
    location = models.TextField()
    picture = models.TextField()

class TeamsBars(models.Model):
    teamId = models.ForeignKey(Teams, on_delete=models.CASCADE)
    barId = models.ForeignKey(Bars, on_delete=models.CASCADE)
