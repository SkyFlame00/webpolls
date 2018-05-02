from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.views.generic import CreateView
from django.forms import formset_factory, BaseFormSet
from django.forms.models import modelformset_factory
from django.db import IntegrityError, transaction
from django import forms

# For use email verification
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site

from .forms import UserForm, UserEducationForm, ProfileForm, LoginForm
from .models import User, UserEducation, Profile

def index(request):
    failedOnFormProcessing = False
    failedOnUserAuthorisation = False
    form = None

    if request.user.is_anonymous:
        if request.method == 'POST':
            # If we receive a filled login form from a user, backend processes it
            form = LoginForm(request.POST)

            if form.is_valid():
                # If all the fields are ok, log in the user
                username = request.POST.get('username', '')
                password = request.POST.get('password', '')
                user = authenticate(username=username, password=password)

                if user is not None:
                    login(request, user)
                    HttpResponseRedirect(reverse('index'))
                else:
                    failedOnUserAuthorisation = True
            else:
                failedOnFormProcessing = True
        else:
            # If a page has only been visited, send them just a login form
            form = LoginForm()

    return render(
        request,
        'index.html',
        {
            'form': form,
            'failedOnFormProcessing': failedOnFormProcessing,
            'failedOnUserAuthorisation': failedOnUserAuthorisation
        }
    )

def logoutView(request):
    logout(request)
    return HttpResponseRedirect(request.GET.get('next', '/'))

def manage_choices(request):
    QuestionFormset = formset_factory(QuestionForm)

    if request.method == 'POST':
        formset = QuestionFormset(request.POST)
        if formset.is_valid():
            pass
    else:
        formset = QuestionFormset()

    return render(
        request,
        'formset-test.html',
        {
            'formset': formset
        }
    )

def signup(request):
    UserEducationFormset = formset_factory(UserEducationForm)

    # Helpful variables
    error = None
    educations = []
    formsAmountLen = 0
    formsAmount = 0
    emptyformsAmount = 0
    educFormsError = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        usereducation_formset = UserEducationFormset(request.POST)

        formsAmountLen = len(usereducation_formset)

        # Do the validation to force cleaned_data attributes be created
        usereducation_formset.is_valid()

        # Check out whether forms are empty
        for education in usereducation_formset:
            field_university = education.cleaned_data.get('university')
            field_degree = education.cleaned_data.get('degree')
            field_educ_start = education.cleaned_data.get('educ_start')
            field_educ_end = education.cleaned_data.get('educ_end')
            field_programme = education.cleaned_data.get('programme')

            formsAmount += 1

            if not field_university and not field_degree and not field_educ_start and not field_educ_end and not field_programme:
                emptyformsAmount += 1

        if formsAmount == 1 and emptyformsAmount == 1:
            error = 'Ваша форма пуста'
            educFormsError = True

        if formsAmount > 0 and emptyformsAmount > 0 and formsAmount != emptyformsAmount:
            error = 'Одна из ваших форм полностью пуста'
            educFormsError = True

        if formsAmount > 1 and formsAmount == emptyformsAmount:
            error = 'Все ваши формы пусты'
            educFormsError = True


        if user_form.is_valid() and profile_form.is_valid() and usereducation_formset.is_valid() and not educFormsError:
            user = user_form.save(commit=False)
            user.is_active = False
            user.save()

            day = profile_form.cleaned_data.get('day_of_birth')
            month = profile_form.cleaned_data.get('month_of_birth')
            year = profile_form.cleaned_data.get('year_of_birth')

            user.profile.patronymic = profile_form.cleaned_data.get('patronymic')
            user.profile.birth_date = '%s-%s-%s' % (year, month, day)
            user.profile.save()

            educations = []

            for education in usereducation_formset:
                educations.append(UserEducation(
                    user=user,
                    university=education.cleaned_data.get('university'),
                    degree=education.cleaned_data.get('degree'),
                    educ_start=education.cleaned_data.get('educ_start'),
                    educ_end=education.cleaned_data.get('educ_end'),
                    programme=education.cleaned_data.get('programme'),
                ))

            try:
                with transaction.atomic():
                    UserEducation.objects.bulk_create(educations)

            except IntegrityError: # If the transaction failed
                return HttpResponse('An error occured while creating your profile')

            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            message = render_to_string('acc_activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            to_email = user_form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()

            # Redirect to a beautiful page is preferred
            return render(
                request,
                'after_signup.html'
            )
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
        usereducation_formset = UserEducationFormset()

    return render(
        request,
        'signup.html',
        {
            'user_form': user_form,
            'profile_form': profile_form,
            'usereducation_formset': usereducation_formset,
            'error': error,
            'emptyformsAmount': emptyformsAmount,
            'formsAmount': formsAmount,
            'formsAmountLen': formsAmountLen
        }
    )

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

def myprofile(request):
    user = request.user
    educations = UserEducation.objects.all().filter(user=user)
    educationsAmount = len(educations)

    return render(
        request,
        'myprofile.html',
        {
            'user': user,
            'profile': user.profile,
            'educations': educations,
            'educationsAmount': educationsAmount
        }
    )

from .forms import UserFormEdit

def myprofile_edit(request):
    user = request.user
    first_name = user.first_name
    last_name = user.last_name
    UserEducationFormset = formset_factory(form=UserEducationForm, extra=0)
    educations = UserEducation.objects.all().filter(user=user).values()
    educationsNum = len(educations)
    educFormsError = False

    birth = user.profile.birth_date
    day_of_birth = birth.strftime('%d')
    month_of_birth = birth.strftime('%m')
    year_of_birth = birth.strftime('%Y')

    formsAmount = 0
    emptyformsAmount = 0

    if request.method == 'POST':
        userform = UserFormEdit(instance=user, data=request.POST)
        profileform = ProfileForm(instance=user.profile, data=request.POST)
        usereducs_formset = UserEducationFormset(request.POST)

        # Do the validation to force cleaned_data attributes be created
        usereducs_formset.is_valid()

        # Check out whether forms are empty
        for education in usereducs_formset:
            field_university = education.cleaned_data.get('university')
            field_degree = education.cleaned_data.get('degree')
            field_educ_start = education.cleaned_data.get('educ_start')
            field_educ_end = education.cleaned_data.get('educ_end')
            field_programme = education.cleaned_data.get('programme')

            formsAmount += 1

            if not field_university and not field_degree and not field_educ_start and not field_educ_end and not field_programme:
                emptyformsAmount += 1

        if formsAmount == 1 and emptyformsAmount == 1:
            error = 'Ваша форма пуста'
            educFormsError = True

        if formsAmount > 0 and emptyformsAmount > 0 and formsAmount != emptyformsAmount:
            error = 'Одна из ваших форм полностью пуста'
            educFormsError = True

        if formsAmount > 1 and formsAmount == emptyformsAmount:
            error = 'Все ваши формы пусты'
            educFormsError = True

        if userform.is_valid() and profileform.is_valid() and usereducs_formset.is_valid() and not educFormsError:
            validated = True
            user = userform.save(commit=False)
            user.save()

            day = profileform.cleaned_data.get('day_of_birth')
            month = profileform.cleaned_data.get('month_of_birth')
            year = profileform.cleaned_data.get('year_of_birth')

            educations = []

            for education in usereducs_formset:
                educations.append(UserEducation(
                    user=user,
                    university=education.cleaned_data.get('university'),
                    degree=education.cleaned_data.get('degree'),
                    educ_start=education.cleaned_data.get('educ_start'),
                    educ_end=education.cleaned_data.get('educ_end'),
                    programme=education.cleaned_data.get('programme'),
                ))

            try:
                with transaction.atomic():
                    UserEducation.objects.all().filter(user=user).delete()
                    UserEducation.objects.bulk_create(educations)

            except IntegrityError: # If the transaction failed
                return HttpResponse('An error occured while creating your profile')

            return redirect('myprofile')
    else:
        userform = UserFormEdit(instance=user)
        profileform = ProfileForm(instance=user.profile, initial={'day_of_birth': day_of_birth, 'month_of_birth': month_of_birth, 'year_of_birth': year_of_birth})
        usereducs_formset = UserEducationFormset(initial=educations)

    return render(
        request,
        'myprofile_edit.html',
        {
            'userform': userform,
            'profileform': profileform,
            'usereducs_formset': usereducs_formset,
            'educationsNum': educationsNum,
            'emptyformsAmount': emptyformsAmount,
            'formsAmount': formsAmount
        }
    )

def testing(request):
    UserEducationFormset = modelformset_factory(model=UserEducation, form=UserEducationForm, extra=1)
    user = request.user
    educs = UserEducation.objects.all().filter(user=user).values()

    if request.method == 'POST':

        formset = UserEducationFormset(request.POST)

        if formset.is_valid():
            formset.save()

            return HttpResponse('Success!')
    else:
        formset = UserEducationFormset(initial=educs)

    return render(
        request,
        'testing.html',
        {
            'formset': formset
        }
    )
