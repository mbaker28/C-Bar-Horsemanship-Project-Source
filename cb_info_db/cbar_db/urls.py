from django.conf.urls import url

from . import views

urlpatterns = [
    # Website index
    url(r'^$', views.index_public, name='index-public'),

    # Public forms index
    url(r'^forms/public/$', views.index_public_forms, name='index-public-forms'),

    # Application form
    url(r'^forms/public/application/$', views.public_form_application,
        name='public-form-application'),

    # Medical Release form
    url(r'^forms/public/med_release/$', views.public_form_med_release,
        name='public-form-med-release'),

    # Emegency Medical Treatment Authorization form
    url(r'^forms/public/emerg_auth/$', views.public_form_emerg_auth,
        name='public-form-emerg-auth'),

    # Liability Release form
    url(r'^forms/public/liability/$', views.public_form_liability,
        name='public-form-liability'),

    # Media Release form
    url(r'^forms/public/media/$', views.public_form_media,
        name='public-form-media'),

    # Background Check Authorization form
    url(r'^forms/public/background/$', views.public_form_background,
        name='public-form-backround'),

    # Seizure Evaluation form
    url(r'^forms/public/seizure/$', views.public_form_seizure,
        name='public-form-seizure'),
]
