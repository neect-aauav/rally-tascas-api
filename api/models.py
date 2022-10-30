from django.db import models

class Teams(models.Model):
	name = models.CharField(max_length=255)
	phone = models.IntegerField()
	points = models.IntegerField(default=0)
	drinks = models.IntegerField(default=0)
	qr_code = models.CharField(max_length=255, default="")
	created = models.DateTimeField(auto_now_add=True)
	has_egg = models.BooleanField(default=True)
	puked = models.IntegerField(default=0)

	# final prizes
	best_name = models.BooleanField(default=False)
	best_team_costume = models.BooleanField(default=False)
	won_special_game = models.BooleanField(default=False)

	def __str__(self):
		return str(self.name)


class Members(models.Model):
	name = models.CharField(max_length=255)
	course = models.CharField(max_length=255)
	nmec = models.IntegerField()
	points = models.IntegerField(default=0)
	drinks = models.IntegerField(default=0)
	team = models.ForeignKey(Teams, on_delete=models.CASCADE)

class Games(models.Model):
	name = models.CharField(max_length=255)
	description = models.TextField(default="")
	points = models.IntegerField(default=0)
	completed = models.IntegerField(default=0)

class Bars(models.Model):
	name = models.CharField(max_length=255)
	address = models.CharField(max_length=255)
	latitude = models.FloatField()
	longitude = models.FloatField()
	picture = models.TextField(default="")
	points = models.IntegerField(default=0)
	drinks = models.IntegerField(default=0)
	puked = models.IntegerField(default=0)
	game = models.ForeignKey(Games, on_delete=(models.CASCADE), default=None, blank=True, null=True)

	def __str__(self):
		return str(self.name)

class TeamsBars(models.Model):
	teamId = models.ForeignKey(Teams, on_delete=models.CASCADE)
	barId = models.ForeignKey(Bars, on_delete=models.CASCADE)
	visited = models.BooleanField(default=False)
	points = models.IntegerField(default=0)
	drinks = models.IntegerField(default=0)
	won_game = models.BooleanField(default=False)
	has_egg = models.BooleanField(default=True)
	puked = models.IntegerField(default=0) 

class MembersBars(models.Model):
	memberId = models.ForeignKey(Members, on_delete=models.CASCADE)
	barId = models.ForeignKey(Bars, on_delete=models.CASCADE)
	points = models.IntegerField(default=0)
	drinks = models.IntegerField(default=0)

class Prizes(models.Model):
	place = models.IntegerField()
	name = models.CharField(max_length=255)
	ammount = models.IntegerField()
	winner = models.ForeignKey(Teams, on_delete=models.CASCADE, default=None, blank=True, null=True)