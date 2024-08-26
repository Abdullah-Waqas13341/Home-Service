from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from sellers.models import Seller
from customers.models import Customer
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'autofocus': True}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Email'

    def clean(self): 
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError('Invalid email or password.')
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data




class SignUpForm(UserCreationForm):
    
    
    
    
    class Meta:
        model = User
        fields = ['username','email' ,'gender','age','password1','password2', 'role']
        gender = forms.ChoiceField(choices=User.GENDER_CHOICES)
        role = forms.ChoiceField(choices=User.ROLE_CHOICES)
        age = forms.IntegerField()
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control custom-input',
                'placeholder': 'Username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control custom-input',
                'placeholder': 'Email Address'
            }),
            'age': forms.NumberInput(attrs={
                'class': 'form-control custom-input',
                'placeholder': 'Age'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-control custom-input'
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control custom-input',
                'placeholder': 'Password',
                'type': 'password' 
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control custom-input',
                'placeholder': 'Confirm Password',
                'type': 'password'  
            }),
            'role': forms.Select(attrs={
                'class': 'form-control custom-input'
            }),
        }
    
    def save(self, commit=True):
        role = self.cleaned_data['role']
        if role == 'seller':
            user = Seller.objects.create(
                username=self.cleaned_data['username'],
                email=self.cleaned_data['email'],
        
                gender=self.cleaned_data['gender'],
                age=self.cleaned_data['age'],
                role=role,
            )
        elif role == 'customer':
            user = Customer.objects.create(
                username=self.cleaned_data['username'],
                email=self.cleaned_data['email'],
                gender=self.cleaned_data['gender'],
                age=self.cleaned_data['age'],
                role=role,
            )
        
        user.set_password(self.cleaned_data['password1'])
        
        if commit:
            user.save()
        
        return user

    
    

   
    
   

