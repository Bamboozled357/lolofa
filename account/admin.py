
from django.contrib.auth import get_user_model
from django import forms
from main import admin

User = get_user_model()



class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email', 'password', 'last_name',
                  'is_active', 'is_staff')

    def save(self, commit=True):
        return User.objects.create_user(**self.cleaned_data)

    def save_m2m(self):
        pass


class UserAdmin(admin.ModelAdmin):
    form = UserForm


