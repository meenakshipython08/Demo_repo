from django.db import models

# Create your models here.
# from django.db import models
# from django.contrib.auth.models import User
# from django.contrib.auth.models import AbstractUser, AbstractBaseUser
 
class scraping_info(models.Model):
	print("Database done")
	saved_files = models.CharField(max_length=100, null=True, blank=True)
	in_progress_files = models.CharField(max_length=100, null=True, blank=True)
	print("created!")
	
