from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from sellers.models import Seller
from customers.models import Customer


from django.contrib.auth.forms import AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control custom-input', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control custom-input', 'placeholder': 'Password'}))

    class Meta:
        model = User
        fields = ['email', 'password']




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
                'type': 'password'  # Add this line to specify the input type as 'password'
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control custom-input',
                'placeholder': 'Confirm Password',
                'type': 'password'  # Add this line to specify the input type as 'password'
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
class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control custom-input',
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control custom-input',
        'placeholder': 'Password'
    }))
    class LoginForm(forms.Form):
        username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control custom-input',
        'placeholder': 'Username'
            }))
        password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control custom-input',
        'placeholder': 'Password'
            }))
    

   
    
   

