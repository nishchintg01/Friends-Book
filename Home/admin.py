from django.contrib import admin
from .models import Profile,Posts,FriendRequest,Comments


class CommentSection(admin.ModelAdmin):
	list_display = ['post','Author','comment']

admin.site.register(Posts)
admin.site.register(Profile)
admin.site.register(FriendRequest)

admin.site.register(Comments,CommentSection)
# Register your models here.
