from django.db import models

# Create your models here.


from django.contrib.auth.models import User
class user_likes(models.Model):
	user = models.CharField(max_length=255)
	like_index= models.IntegerField()
	
	def __str__(self):
		return self.user