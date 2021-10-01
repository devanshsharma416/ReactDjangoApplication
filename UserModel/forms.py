from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import NewUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = NewUser
        fields = "__all__"


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = NewUser
        fields = "__all__"


class NewForm(UserCreationForm):
    class Meta:
        model = NewUser
        fields = ('email', 'first_name', 'last_name')