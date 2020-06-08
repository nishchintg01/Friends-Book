from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate ,get_user_model,logout,update_session_auth_hash
from django.contrib.auth import login as Auth_login
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile,FriendRequest,Comments,Posts
from .forms import LoginForm,CommentForm,ProfileEditForm
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.contrib.auth.forms import PasswordChangeForm

#Login Page
def login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		try:
		    user = authenticate(request , username=username,password=password)
		    if user is not None:
		        Auth_login(request,user)
		        return redirect('home')
		    else:
		        messages.info(request,"Wrong Information! Try again")
		        return redirect('intro')
		except:
		    messages.info(request,"User Does not Exist! Try again")
		    return redirect('intro')
	return redirect('intro')

#Signup Form
def SignupForm(request):
	form = LoginForm()
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('intro')
		else:
			messages.info(request,'Invalid Credentials! Try Again')
	else:
		return render(request,'authentication/Signup.html',{'form':form})

	return render(request,'authentication/Signup.html',{'form':form})


#Friends Book Homepage View
@login_required(login_url='intro')
def Home(request):
	profile = Profile.objects.get_or_create(user=request.user)
	posts = Posts.objects.all().order_by('-Updated_on')
	form = CommentForm()
	p = Profile.objects.filter(user=request.user).first()
	friend = p.friends.all()
	friends =[]
	for name in friend:
		friends.append(name.username)
	users = User.objects.all().exclude(username=request.user.username)
	not_friend = []
	for user in users:
		if user.username in friends:
			pass
		else:
			not_friend.append(user)
	context = {
		'articles':posts,
		'form':form,
		'friends_list': not_friend[:4],
	}
	return render(request, "home/homepage.html", context)

# Update User Details
@login_required(login_url='intro')
def UpdateUser(request):
	if request.method == 'POST':
		profile = Profile.objects.get(user = request.user)
		username = request.POST['username']
		fname = request.POST['fname']
		lname = request.POST['lname']
		email = request.POST['email']
		user = User.objects.get(username=request.user.username)
		if username:
			user.username = username
		if fname:
			user.first_name = fname
		if lname:
			user.last_name = lname
		if email:
			user.email = email
		user.save()
		profile.save()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
# Edit Your Profile Form

@login_required(login_url='intro')
def ProfileForm(request,username):
	user = Profile.objects.get_or_create(user = request.user)
	if request.method=='POST':
		form  = ProfileEditForm(request.POST,request.FILES,instance=request.user.profile)
		if form.is_valid():
			form.save()
			return redirect('editprofile',username=request.user.username)
		else:
			form  = ProfileEditForm(instance=request.user.profile)
			return render(request,'home/profiledit.html',{'form':form})
	form  = ProfileEditForm(instance=request.user.profile)
	Userform = LoginForm(instance=request.user)
	changepasswordform = PasswordChangeForm(request.user, request.POST)
	return render(request,'home/profiledit.html',{'form':form,'userform':Userform,'changepasswordform':changepasswordform})

def testtingpage(request):
	return render(request,'home/Text.html')


# Like In a Post
@login_required()
def like(request,id):
    try:
        post = get_object_or_404(Posts,id=id)
        post.Likes.add(request.user)
    except:
        messages.info(request,'Cannot like this Post! Try Again')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# Delete existing Status
@login_required(login_url='intro')
def DeletePost(request,slug):
    try:
        post = get_object_or_404(Posts,slug=slug)
        post.delete()
    except:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# Send Request to a User
@login_required(login_url='intro')
def Send_request(request,id):
    try:
        if request.user.is_authenticated:
            user = get_object_or_404(User,id=id)
            Frequest,created = FriendRequest.objects.get_or_create(
			                    from_user = request.user,
			                    to_user = user,
			                    Sent_request=True
			                    )
            messages.success(request,f'Friend request has been sent to {user.username}')
    except:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# Cancel Sent Request to a Existing User
@login_required(login_url='intro')
def Cancel_request(request,id):
	if request.user.is_authenticated:
		user = get_object_or_404(User,id=id)
		Frequest= FriendRequest.objects.filter(
			from_user = request.user,
			to_user = user
			).first()
		Frequest.delete()
		messages.success(request,f'Friend request cancelled {user.username}')
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# Accept User Friend Request
@login_required(login_url='intro')
def Accept_friend_request(request,id):
    try:
        from_user = get_object_or_404(User,id=id)
        frequest = FriendRequest.objects.filter(from_user=from_user,to_user=request.user).first()
        user1 = frequest.to_user
        user2 = from_user
        user1.profile.friends.add(user2.profile)
        user2.profile.friends.add(user1.profile)
        frequest.delete()
    except:
        messages.success(request,f'Friend request already sent {request.user.username}')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# Delete Friend Request from User
@login_required(login_url='intro')
def Delete_friend_request(request,id):
	from_user = get_object_or_404(User,id=id)
	frequest = FriendRequest.objects.filter(from_user=from_user,to_user = request.user).first()
	frequest.delete()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# Delete a Friend
@login_required(login_url='intro')
def Delete_friend(request,id):
	user= User.objects.get(id=request.user.id)
	friends = user.profile.friends.get(id=id)
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



# User Profile Page View
@login_required(login_url='intro')
def User_Profile(request,username):
	if request.user.is_authenticated:
		user = User.objects.get(username=request.user.username)
		try:
			friends = user.profile.friends.all()
		except:
			friends=None
		return render(request,'home/usertimeline.html',{'user':request.user})
	else:
		return redirect('intro')

# Upload a new Status
@login_required(login_url='intro')
def Status(request):
	if request.method == 'POST':
		text = request.POST['status']
		post = Posts(Status=text,Author=request.user)
		post.save()
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	return redirect('home')

# Make New Comment
@login_required(login_url='intro')
def make_comment(request,slug):
	posts = get_object_or_404(Posts,slug=slug)
	if request.method == "POST":
		form = CommentForm(request.POST)
		if form.is_valid():
			new_comment = form.save(commit=False)
			new_comment.Author = request.user
			new_comment.post = posts
			new_comment.save()
			return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	else:
		return request('home')
	return redirect('home')


# Edit User Profile Form
@login_required(login_url='intro')
def UserProfileForm(request,username):
	if request.method=='POST':
		form  = LoginForm(request.POST,instance=profile)
		if form.is_valid:
			form.save()
			return redirect('profile',username=username)
		else:
			return render(request,'authentication/editprofile.html',{'form':form})
	form = LoginForm(instance=request.user)
	return render(request,'authentication/editprofile.html',{'form':form})


# Myposts Page View
@login_required(login_url='intro')
def myposts(request):
	p = Profile.objects.filter(user=request.user).first()
	form = CommentForm()
	posts = Posts.objects.filter(Author = request.user).order_by('-Updated_on')
	rec_friend_requests = FriendRequest.objects.filter(to_user=p.user)
	friends = p.friends.all()
	return render(request,'home/usertimeline.html',{'friends':friends,
		'posts':posts,'form':form,'rec_friend_requests':rec_friend_requests,'profile':p})

# Search user Page View
@login_required(login_url='intro')
def Search(request):
	if request.method=='POST':
		term = request.POST['srch-term']
		users = Profile.objects.filter(Q(Full_name__icontains=term)|Q(username__icontains=term)).exclude(user=request.user)
		if users:
			paginator = Paginator(users,10)
			page = request.GET.get('page')
			users = paginator.get_page(page)
			return render(request,'home/search_results.html',{'users':users,'term':term})
		else:
			return render(request,'home/user_not_found.html',{'term':term})


	return render(request,'home/search_results.html')

def GetUserProfile(request,user):
	#print(request.build_absolute_uri())
	profile = Profile.objects.get(username=user)
	is_friend = False
	for friend in profile.friends.all():
		if request.user.username == friend.username:
			is_friend = True
	friends=profile.friends.all()
	author = User.objects.filter(username=user).first()
	posts = Posts.objects.filter(Author=author)
	form = CommentForm()
	return render(request,'home/getuserprofile.html',{'profile':profile,'is_friend':is_friend,
		'friends':friends,'posts':posts,'form':form,'author':author})


def DeleteFriend(request,user):
	from_user = get_object_or_404(User,id=user)
	user1= from_user
	user2 = request.user
	user1.profile.friends.remove(user2.profile)
	user2.profile.friends.remove(user1.profile)
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# Password Change View
def Change_Password(request):
	if request.method == "POST":
		try:
			form = PasswordChangeForm(request.user,request.POST)
			if form.is_valid():
				user=form.save()
				update_session_auth_hash(request,user)
				messages.success(request,"User password Changed Succesfully")
			messages.success(request,"The password you provided didn't match ! Try Again")
		except:
			messages.success(request,"The password you provided didn't match ! Try Again")
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

