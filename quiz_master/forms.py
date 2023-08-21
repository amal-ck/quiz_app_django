from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import QuizModel, QuestionModel

User = get_user_model()

class MasterRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class MasterLoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)
    remember_me = forms.BooleanField(required=False)

class QuizForm(forms.ModelForm):
    time = forms.TimeField(initial='01:00')
    class Meta:
        model = QuizModel
        fields = '__all__'
class QuestionForm(forms.ModelForm):
    class Meta:
        model = QuestionModel
        fields  = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quiz'].queryset = QuizModel.objects.all()
        self.fields['quiz'].widget = forms.HiddenInput()
        