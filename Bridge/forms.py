from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegisterForm(UserCreationForm):
    """
    Form for user registration.
    
    Args:
        UserCreationForm: Django's built-in form for creating users.
    """
    email = forms.EmailField(required=True)
    
    # Customize field names to match the template
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class LoginForm(forms.Form):
    """
    Form for user login.
    
    Includes fields for username and password.
    """
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class NewClassForm(forms.Form):
    """
    Form for creating a new class.
    
    Includes fields for class name, location, and background image upload.
    """
    class_name = forms.CharField(max_length=100, required=True)
    location = forms.CharField(max_length=100, required=True)
    class_picture = forms.ImageField(required=False)  # Changed to ImageField for file uploads


class AddModuleForm(forms.Form):
    """
    Form for adding a new module to a class.
    
    Includes fields for title, description, content, and order.
    """
    title = forms.CharField(max_length=100, required=True)
    description = forms.CharField(widget=forms.Textarea, required=True, 
                                help_text="Supports Markdown formatting")
    content = forms.CharField(widget=forms.Textarea, required=True, 
                            help_text="Supports Markdown formatting")
    order = forms.IntegerField(initial=0, required=False, 
                            help_text="Modules are displayed in ascending order")


class AddStudentForm(forms.Form):
    """
    Form for adding a student to a class.
    
    Includes field for student username.
    """
    student_username = forms.CharField(max_length=150, required=True)  # Match template field name


class EditHomepageForm(forms.Form):
    """
    Form for editing the homepage content of a class.
    
    Includes field for homepage content.
    """
    # Using hyphen to match template field name
    home_content = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Change the field name to match the template
        if 'home_content' in self.fields:
            self.fields['home-content'] = self.fields.pop('home_content')