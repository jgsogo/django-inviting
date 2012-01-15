from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module


def get_module_object(mod_obj_path):
    module_name, obj_name = mod_obj_path.rsplit('.', 1)
    try:
        object = getattr(import_module(module_name), obj_name)
    except ImportError:
        raise ImproperlyConfigured('Can\'t import module `%s`' % module_name)
    except AttributeError:
        raise ImproperlyConfigured('Can\'t import ' \
                                   '`%s` from `%s`' % (obj_name,
                                                       module_name))
    return object

def get_registration_form():
    if isinstance(REGISTRATION_FORM, (str, unicode)):
        return get_module_object(REGISTRATION_FORM)
    return REGISTRATION_FORM

def get_performance_func(settings):
    performance_func = getattr(settings, 'INVITATION_PERFORMANCE_FUNC', None)
    if isinstance(performance_func, (str, unicode)):
        performance_func = get_module_object(performance_func)
    if performance_func and not callable(performance_func):
        raise ImproperlyConfigured('INVITATION_PERFORMANCE_FUNC must be a ' \
                                   'callable or an import path string ' \
                                   'pointing to a callable.')
    return performance_func


REGISTRATION_FORM = getattr(settings, 'INVITATION_REGISTRATION_FORM',
                            'registration.forms.RegistrationForm')
INVITE_ONLY = getattr(settings, 'INVITATION_INVITE_ONLY', False)
EXPIRE_DAYS = getattr(settings, 'INVITATION_EXPIRE_DAYS', 15)
INITIAL_INVITATIONS = getattr(settings, 'INVITATION_INITIAL_INVITATIONS', 10)
REPOPULATE_ACCEPTED = getattr(settings, 'INVITATION_REPOPULATE_ACCEPTED', False)
AUTO_LOGIN = getattr(settings, 'INVITATION_AUTO_LOGIN', False)
REWARD_THRESHOLD = getattr(settings, 'INVITATION_REWARD_THRESHOLD', 0.75)
PERFORMANCE_FUNC = get_performance_func(settings)
AUTH_CREATE_USER_FUNC = getattr(settings, 'AUTH_CREATE_USER_FUNC',
    get_module_object("django.contrib.auth.models.User").objects.create_user)
