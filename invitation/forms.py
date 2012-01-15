from django import forms
from django.contrib.auth.models import User
from . import app_settings


def save_user(form_instance, profile_callback=None):
    """
    Create a new **active** user from form data.

    This method is intended to replace the ``save`` of
    ``django-registration``s ``RegistrationForm``. Calls
    ``profile_callback`` if provided. Required form fields
    are ``username``, ``email`` and ``password1``.
    """
    
    password = form_instance.cleaned_data['password1']
    create_user_func = getattr(app_settings, 'AUTH_CREATE_USER_FUNC')
    if isinstance(create_user_func, basestring):
        create_user_func = app_settings.get_module_object(create_user_func)
    if create_user_func:
        new_user = create_user_func(password=password,
                                    **form_instance.cleaned_data)
        return new_user


class InvitationForm(forms.Form):
    email = forms.EmailField()


class RegistrationFormInvitation(app_settings.get_registration_form()):
    """
    Subclass of ``registration.RegistrationForm`` that create an **active**
    user.

    Since registration is (supposedly) done via invitation, no further
    activation is required. For this reason ``email`` field always return
    the value of ``email`` argument given the constructor.
    """
    def __init__(self, email, *args, **kwargs):
        super(RegistrationFormInvitation, self).__init__(*args, **kwargs)
        self._make_email_immutable(email)

    def _make_email_immutable(self, email):
        self._email = self.initial['email'] = email
        if 'email' in self.data:
            self.data = self.data.copy()
            self.data['email'] = email
        self.fields['email'].widget.attrs.update({'readonly': True})

    def clean_email(self):
        return self._email

    save = save_user
