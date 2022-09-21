from django import forms
from django.core.exceptions import ValidationError

from studentskillsharing.models import Profile


def clean_user_handle(user_handle):
    user_model = Profile
    try:
        user_model.objects.get(user_handle_iexact=user_handle)
    except user_model.DoesNotExist:
        return user_handle
    raise forms.ValidationError("This username is taken.")


def clean_user_email(user_email):
    email_domain = user_email.split('@')[1]

    if email_domain != 'virginia.edu':
        raise forms.ValidationError('You must use a virginia.edu email address')

    return user_email

# class SignUpForm(forms.ModelForm):
#         class Meta:
#             model = Profile
#             fields = ('first_name', 'last_name', 'user_email', 'user_handle', 'bio_text')
#
#         def clean(self):
#             model = Profile
#             email = self.cleaned_data.get('user_email')
#             handle = self.cleaned_data.get('user_handle')
#
#             email_domain = email.split('@')[1]
#             if email_domain != 'virginia.edu':
#                 raise ValidationError('You must use a virginia.edu email address')
#
#             # try:
#             #     model.objects.get(user_handle_iexact=handle)
#             # except model.DoesNotExist:
#             #     return handle
#             # raise forms.ValidationError("This username is taken.")
#
#
# def clean_user_handle(user_handle):
#     user_model = Profile
#     try:
#         user_model.objects.get(user_handle_iexact=user_handle)
#     except user_model.DoesNotExist:
#         return user_handle
#     raise forms.ValidationError("This username is taken.")
#
#
# def clean_user_email(user_email):
#     email_domain = user_email.split('@')[1]
#
#     if email_domain != 'virginia.edu':
#         raise forms.ValidationError('You must use a virginia.edu email address')
#
#     return user_email

