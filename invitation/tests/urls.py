from django.conf.urls.defaults import *
import invitation.urls as invitation_urls


urlpatterns = invitation_urls.urlpatterns + patterns('',
    url(r'^register/$',
        'django.shortcuts.render',
        {'template': 'registration/registration_register.html'},
        name='registration_register'),
    url(r'^register/complete/$',
        'django.shortcuts.render',
        {'template': 'registration/registration_complete.html'},
        name='registration_complete'),
)
