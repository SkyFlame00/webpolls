from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.conf import settings

from .models import User, Profile, UserEducation
from .choices import *

class LoginForm(forms.Form):
    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())

class UserForm(forms.ModelForm):
    username = forms.CharField(required=False)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    password_confirmation = forms.CharField(widget=forms.PasswordInput(), required=False)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        existing_user = User.objects.all().filter(username=username)

        if not username:
            raise forms.ValidationError('Поле не может быть пустым')

        if existing_user:
            raise forms.ValidationError('Пользователь с таким никнеймом уже существует')

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if not email:
            raise forms.ValidationError('Поле не может быть пустым')

        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if len(password) < 6:
            raise forms.ValidationError('Пароль должен содержать не менее 6 символов')

        return password

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')

        if not first_name:
            raise forms.ValidationError('Поле не может быть пустым')

        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')

        if not last_name:
            raise forms.ValidationError('Поле не может быть пустым')

        return last_name

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')

        error_list = []

        if password != password_confirmation and password != None:
            error_list.append('Пароли не совпадают')

        if error_list:
            raise forms.ValidationError(error_list)


class UserFormEdit(forms.ModelForm):
    #password = forms.CharField(required=False)
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

class DateInput(forms.DateInput):
    input_type = 'date'

class ProfileForm(forms.ModelForm):
    day_of_birth = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'День', 'type': 'number'}), required=False, min_value=1, max_value=31)
    month_of_birth = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Месяц', 'type': 'number'}), required=False, min_value=1, max_value=12)
    year_of_birth = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Год', 'type': 'number'}), required=False, min_value=1900, max_value=2018)

    class Meta:
        model = Profile
        fields = ('patronymic',)

    def clean_day_of_birth(self):
        day_of_birth = self.cleaned_data['day_of_birth']

        if not day_of_birth:
            raise forms.ValidationError('Поле "День" не может быть пустым')

        return day_of_birth

    def clean_month_of_birth(self):
        month_of_birth = self.cleaned_data['month_of_birth']

        if not month_of_birth:
            raise forms.ValidationError('Поле "Месяц" не может быть пустым')

        return month_of_birth

    def clean_year_of_birth(self):
        year_of_birth = self.cleaned_data['year_of_birth']

        if not year_of_birth:
            raise forms.ValidationError('Поле "Год" не может быть пустым')

        return year_of_birth

    def clean(self):
        cleaned_data = super(ProfileForm, self).clean()
        day_of_birth = cleaned_data.get('day_of_birth')
        month_of_birth = cleaned_data.get('month_of_birth')
        year_of_birth = cleaned_data.get('year_of_birth')

        error_list = []

        if year_of_birth and month_of_birth and day_of_birth:
            try:
                import datetime
                datetime.datetime(year_of_birth, month_of_birth, day_of_birth)
            except ValueError:
                error_list.append('Дата рождения введена некорректно')

        if error_list:
            raise forms.ValidationError(error_list)

class UserEducationForm(forms.ModelForm):
    educ_start = forms.IntegerField(required=False, min_value=1900, max_value=2025)
    educ_end = forms.IntegerField(required=False, min_value=1900, max_value=2025)

    class Meta:
        model = UserEducation
        fields = (
            'university',
            'degree',
            'educ_start',
            'educ_end',
            'programme'
        )

    def clean_university(self):
        university = self.cleaned_data.get('university')

        if not university:
            raise forms.ValidationError('Поле не может быть пустым')

        return university

    def clean_degree(self):
        degree = self.cleaned_data.get('degree')

        if not degree:
            raise forms.ValidationError('Поле не может быть пустым')

        return degree

    def clean_educ_start(self):
        educ_start = self.cleaned_data.get('educ_start')

        if not educ_start:
            raise forms.ValidationError('Поле не может быть пустым')

        return educ_start

    def clean_educ_end(self):
        educ_end = self.cleaned_data.get('educ_end')

        if not educ_end:
            raise forms.ValidationError('Поле не может быть пустым')

        return educ_end

    def clean_programme(self):
        programme = self.cleaned_data.get('programme')

        if not programme:
            raise forms.ValidationError('Поле не может быть пустым')

        return programme
