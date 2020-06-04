from django.contrib import admin
from django.urls import path,include
from .views import ( login,Home,User_Profile,Send_request,
					Cancel_request,Accept_friend_request,
					Delete_friend_request,Status,make_comment,SignupForm
					,ProfileForm,UserProfileForm,myposts,like,
					DeletePost,Search,GetUserProfile,testtingpage,UpdateUser,DeleteFriend)
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
		path('Profilepicture',UpdateUser,name="updateuser"),
		path('Post',Status,name='writepost'),
		path('Search/',Search,name="search"),
		path('userprofile/<str:user>',GetUserProfile,name="getuserprofile"),
		path('Post/<slug:slug>',DeletePost,name="delete"),
		path('like/<int:id>',like,name='like'),
		path('myposts',myposts,name="timeline"),
		path('<str:username>/Basic/edit',ProfileForm,name='editprofile'),
		path('<str:username>/User/edit',UserProfileForm,name='edituserprofile'),
		path('Logout',LogoutView.as_view(), name='logout'),
		path('comment/<slug:slug>',make_comment,name="writecomment"),
		path('LoginSignup',TemplateView.as_view(template_name='authentication/login.html'),name='intro'),
		path('Signup',SignupForm,name="signup"),
		path('Login',login,name='login'),
		path('',Home,name='home'),
		path('<str:username>',User_Profile,name='profile'),
		path('Friend-request/Send/<int:id>',Send_request,name="send_request"),
		path('Friend-request/Cancel/<int:id>',Cancel_request,name="cancel_request"),
		path('Friend-request/Accept/<int:id>',Accept_friend_request,name="accept_request"),
		path('Friend-request/Delete/<int:id>',Delete_friend_request,name="delete_request"),
		path('removeFriend/<int:user>',DeleteFriend,name="removefriend"),
	    # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
	    path('password_change/done/',auth_views.PasswordChangeDoneView.as_view(template_name='authentication/passwordchangedone.html'), 
	        	name='password_change_complete'),
	    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='authentication/passwordchange.html'), 
	        	name='password_change'),
	    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='authentication/passwordresetdone.html'),
	     		name='password_reset_done'),
	    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='passwordresetconfirm'),
	    path('password_reset/', auth_views.PasswordResetView.as_view(), name='passwordreset'),
	    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='authentication/passwordresetcomplete.html'),
	     		name='password_reset_complete'),
		

]
