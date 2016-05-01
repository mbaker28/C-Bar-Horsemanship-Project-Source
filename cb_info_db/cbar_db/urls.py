from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    ######################### Publicly accessible #########################
    # Website index
    url(r'^$', views.index_public, name='index-public'),

    # Public forms index
    url(r'^forms/public/$', views.index_public_forms, name='index-public-forms'),

    # Form saved message
    url(r'^forms/saved/$', views.form_saved, name='form-saved'),

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
        name='public-form-background'),

    # Seizure Evaluation form
    url(r'^forms/public/seizure/$', views.public_form_seizure,
        name='public-form-seizure'),

	# Donation form index
    url(r'^forms/public/donation/$', views.donation_index,
        name='donation-index'),

    # Adopt a Participant donation form
    url(r'^forms/public/donation/participant$', views.donation_participant,
        name='donation-participant'),

    # Adopt a Horse donation form
    url(r'^forms/public/donation/horse$', views.donation_horse,
        name='donation-horse'),

    # Monetary donation form
    url(r'^forms/public/donation/monetary$', views.donation_monetary,
        name='donation-monetary'),


    ######################### User login required #########################
    # Login page
    url(r'^user/login/$', auth_views.login,
        {'template_name': 'cbar_db/admin/login.html'},
        name='user-login'),

    # Admin index page
    url(r'^admin/$', views.index_private_admin,
        name='index-private-admin'),

    # Participant record overview page
    url(r'^admin/participant/(?P<participant_id>[0-9]+)/$',
        views.participant_record,
        name='participant-record'),

    # Media Release form report view
    url(r'^admin/participant/(?P<participant_id>[0-9]+)/report/media/(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)/$',
        views.report_media_release,
        name='report-media-release'),

    # Emergency Medical Treatment Authorization form report view
    url(r'^admin/participant/(?P<participant_id>[0-9]+)/report/emerg_auth/(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)/$',
        views.report_emerg_auth,
        name='report-emerg-auth'),

    # Medical Release form report view
    url(r'^admin/participant/(?P<participant_id>[0-9]+)/report/med_release/(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)/$',
        views.report_med_release,
        name='report-med-release'),

    # Liability Release form report view
    url(r'^admin/participant/(?P<participant_id>[0-9]+)/report/liability/(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)/$',
        views.report_liability,
        name='report-liability'),

    # Background Check Authorization form report view
    url(r'^admin/participant/(?P<participant_id>[0-9]+)/report/background/(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)/$',
        views.report_background,
        name='report-background'),

    # Seizure Evaluation form report view
    url(r'^admin/participant/(?P<participant_id>[0-9]+)/report/seizure/(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)/$',
        views.report_seizure,
        name='report-seizure'),

    #Observation Evaluation
    url(r'^forms/private/observation_evaluation/(?P<participant_id>[0-9]+)/$',
        views.observation_evaluation,
        name='private-form-observation-evaluation'),
]
