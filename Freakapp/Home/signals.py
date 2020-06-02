from django.db.models.signals import post_save,pre_save
from Home.models import Profile
from django.dispatch receiver
from django.contrib.auth.models import User

@receiver(post_save,sender=User)
def Create_profile(sender,instance,created,*args,**kwargs):
	if created:
		Profile.objects.create(user=instance)

@receiver(post_save,sender=User)
def Created(sender,instance,*args,**kwargs):
	instance.profile.save()