from django import forms 
from .models import Comments,Profile,Posts
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CommentForm(forms.ModelForm):
	comment = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control rounded-corner','placeholder':'Write your comment here..'}))
	class Meta:
		model = Comments
		fields=['comment']

class LoginForm(UserCreationForm):
	username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'Username'}))
	first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'First Name'}))
	last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'Last Name'}))
	email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder': 'Email'}))
	password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder': 'Password'}))
	password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder': 'Confirm Password'}))

	class Meta:
		model  = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

BIRTH_YEAR_CHOICES = ['2021','2020','2019','2018','2017','2016','2015','2014','2013','2012','2011','2010',
'2009','2008','2007','2006','2005','2004','2003','2002','2001','2000','1999','1998','1997','1996','1995',
'1994','1993','1992','1991','1990','1989','1988','1987','1986','1985','1984','1983','1982','1981','1980', 
'1979','1978', '1977','1976','1975','1974','1973','1972','1971',]


class ProfileEditForm(forms.ModelForm):
    birth_day = forms.DateField(widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES))
    class Meta:
    	model = Profile
    	fields =['Profile_pic','cover_pic','Phone','Address','website','Gender','bio','Profession','Relation_status']

