from django.db import models
from django.contrib.auth.models import User ,AbstractUser
from django.utils.text import slugify
from django.conf import settings
from django.utils import timezone
from django.db.models.signals import post_save,pre_save


GENDER = [
	('Male','Male'),
	('Female','Female'),
	('Others','Others'),
]

class Posts(models.Model):
	Status = models.TextField()
	Author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE,related_name='posts')
	Updated_on = models.DateTimeField(auto_now=True)
	TimeStamp = models.DateTimeField(auto_now_add=True)
	slug = models.SlugField(unique=True,null=True,blank=True,editable=False)
	Likes = models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name='likes')
	Views = models.BigIntegerField(default=0)
	Total_likes = models.BigIntegerField(default=0)


	def __str__(self):
		return self.Status

	class Meta:
		verbose_name_plural = 'Posts'

	def save(self,*args,**kwargs):  
		if not self.slug and self.Status:
			self.slug  = slugify(self.Status)
		super(Posts,self).save(*args,**kwargs)


Realtionship_status = [
	('Single','Single'),
	('Married','Married'),
	("It's Complicated","It's Complicated" )
]

class Profile(models.Model):
	Profile_pic= models.ImageField(upload_to='Profilepics/',default='default_profile.png')
	cover_pic = models.ImageField(upload_to='coverpics/',default='default_cover.png')
	user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='profile')
	username = models.CharField(max_length=100,unique=True,editable=False)
	Full_name = models.CharField(max_length= 200)
	Email = models.EmailField(unique=True)
	Phone = models.BigIntegerField(unique=True,null=True)
	Address = models.CharField(max_length=1000,blank=True,null=True)
	website = models.CharField(max_length=200,blank=True,null=True)
	Gender = models.CharField(choices = GENDER,max_length=100,null=True)
	bio = models.TextField(blank=True,null=True)
	Profession = models.CharField(max_length=200,blank=True,null=True)
	Birth_day = models.DateField(blank=True,null=True)
	Relation_status = models.CharField(choices=Realtionship_status,max_length=100,blank=True,null=True)
	Is_Active = models.BooleanField(default=False)
	friends = models.ManyToManyField('Profile',blank=True)
	Is_friend = models.BooleanField(default=False)

	def __str__(self):
		return self.username

	def save(self,*args,**kwargs):
		self.username = self.user.username
		self.Full_name = self.user.first_name + ' ' + self.user.last_name
		self.Email = self.user.email
		super(Profile,self).save(*args,**kwargs)

class FriendRequest(models.Model):
	from_user =models.ForeignKey(settings.AUTH_USER_MODEL,related_name='from_user',on_delete=models.CASCADE) 
	to_user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='to_user',on_delete=models.CASCADE)
	Time_stamp = models.DateTimeField(auto_now_add=True)
	Sent_request = models.BooleanField(default = False)

	def __str__(self):
		return f"from {self.from_user.username} to {self.to_user.username}"

class Comments(models.Model):
	post = models.ForeignKey(Posts,related_name='comments',on_delete=models.CASCADE)
	Author = models.ForeignKey(settings.AUTH_USER_MODEL,related_name="author",on_delete=models.CASCADE)
	comment = models.CharField(max_length=10000)
	Time_stamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.Author