from django import forms
from django.forms import widgets
from .models import Account, Student
from PIL import Image


class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Your Password',
        'class': 'form-control',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password'
    }))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name',
                  'email', 'phone_number', 'password']

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password doesnot match!"
            )


class AdmissionForm(forms.Form):
    # Personal Details
    name = forms.CharField(max_length=200)
    father_name = forms.CharField(max_length=200, required=False)
    mother_name = forms.CharField(max_length=200, required=False)
    father_occupation = forms.CharField(max_length=200, required=False)
    mother_occupation = forms.CharField(max_length=200, required=False)
    # mailing_address = forms.EmailField()
    address = forms.CharField(widget=widgets.Textarea)
    dob = forms.DateField()
    gender = forms.CharField(max_length=20,)
    course = forms.CharField(max_length=50)
    profile_photo = forms.ImageField(required=False)

    # Academic details 
    x_board = forms.CharField(max_length=200)
    x_year = forms.CharField(max_length=20)
    x_subjects = forms.CharField(max_length=300)
    x_percentage = forms.DecimalField(max_digits=5, decimal_places=2)

    xii_board = forms.CharField(max_length=200)
    xii_year = forms.CharField(max_length=20)
    xii_subjects = forms.CharField(max_length=300)
    xii_percentage = forms.DecimalField(max_digits=5, decimal_places=2)

    degree_university = forms.CharField(max_length=200)
    degree_year = forms.CharField(max_length=20)
    degree_subjects = forms.CharField(max_length=300)
    degree_percentage = forms.DecimalField(max_digits=5, decimal_places=2)

    pg_university = forms.CharField(max_length=200, required=False)
    pg_year = forms.CharField(max_length=20, required=False)
    pg_subjects = forms.CharField(max_length=300, required=False)
    pg_percentage = forms.DecimalField(max_digits=5, decimal_places=2, required=False)

    other_university = forms.CharField(max_length=200, required=False)
    other_year = forms.CharField(max_length=20, required=False)
    other_subjects = forms.CharField(max_length=300, required=False)
    other_percentage = forms.DecimalField(max_digits=5, decimal_places=2, required=False)

    # custom validation to profile_photo field
    def clean_profile_photo(self):
        profile = self.cleaned_data.get('profile_photo', False)
        if profile:
            if (profile.size * 0.001) > 250:
                raise forms.ValidationError(
                    'Profile photo size should be less then 250kb',
                    code='invalid_profile_photo_size',
                )
            
            return profile
        